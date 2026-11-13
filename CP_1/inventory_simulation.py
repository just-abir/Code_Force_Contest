"""
(s, S) Inventory Policy Simulation
====================================
Discrete-event simulation of a single-product inventory system
using the stationary (s, S) review policy.

Events modelled
---------------
1. Demand Arrival   – a customer arrives and requests a random quantity
2. Monthly Review   – check inventory; place an order if I < s
3. Order Arrival    – outstanding order lands; clear backlog first

Costs
-----
- Ordering  : K + c * Q  when Q > 0, else 0
- Holding   : h * (positive inventory) * time_fraction
- Shortage  : p * (backlog) * time_fraction

Author  : generated for teaching purposes
"""

import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# 1.  Demand-size distribution  (discrete empirical)
# ---------------------------------------------------------------------------
#
# Requirement 4 says "replace this section with the demand distribution
# provided in the assignment."  A representative distribution is supplied
# below; edit DEMAND_SIZES and DEMAND_PROBS to match your assignment.
#
DEMAND_SIZES = [1, 2, 3, 4]          # possible demand quantities
DEMAND_PROBS = [0.25, 0.35, 0.25, 0.15]  # corresponding probabilities


# ---------------------------------------------------------------------------
# 2.  Event type constants
# ---------------------------------------------------------------------------
EVENT_DEMAND = "Demand Arrival"
EVENT_REVIEW = "Monthly Review"
EVENT_ORDER  = "Order Arrival"


# ---------------------------------------------------------------------------
# 3.  Data classes
# ---------------------------------------------------------------------------

@dataclass(order=True)
class Event:
    """
    A single simulation event stored in the priority queue (min-heap).

    Attributes
    ----------
    time       : scheduled clock time of the event
    event_type : one of EVENT_DEMAND, EVENT_REVIEW, EVENT_ORDER
    order_qty  : quantity carried by an ORDER_ARRIVAL event (0 otherwise)
    """
    time: float
    event_type: str = field(compare=False)
    order_qty: int  = field(default=0, compare=False)


@dataclass
class SimStats:
    """Accumulators updated after every event."""
    total_ordering_cost: float  = 0.0
    total_holding_cost:  float  = 0.0
    total_shortage_cost: float  = 0.0
    num_orders:          int    = 0
    total_demand:        int    = 0
    demand_satisfied:    int    = 0
    # time-weighted integrals (for average inventory / backlog)
    inventory_area:      float  = 0.0   # sum of I+ * dt
    backlog_area:        float  = 0.0   # sum of B  * dt


# ---------------------------------------------------------------------------
# 4.  InventorySystem class
# ---------------------------------------------------------------------------

class InventorySystem:
    """
    Simulates an (s, S) inventory system using a discrete-event engine.

    Parameters
    ----------
    s          : reorder point
    S          : order-up-to level
    n_months   : simulation horizon (months)
    h          : holding cost per unit per month
    p          : shortage cost per unit per month
    K          : fixed ordering (setup) cost
    c          : unit ordering cost
    mean_iat   : mean inter-arrival time of customers (months)
    rng_seed   : NumPy random seed for reproducibility
    """

    def __init__(
        self,
        s: int,
        S: int,
        n_months: int,
        h: float,
        p: float,
        K: float = 32.0,
        c: float = 3.0,
        mean_iat: float = 0.1,
        rng_seed: Optional[int] = None,
    ):
        # --- policy parameters ---
        self.s = s
        self.S = S
        self.n_months = n_months
        self.h = h
        self.p = p
        self.K = K
        self.c = c
        self.mean_iat = mean_iat

        # --- RNG ---
        self.rng = np.random.default_rng(rng_seed)

        # --- state variables ---
        self.clock:           float = 0.0
        self.inventory:       int   = S        # start full
        self.backlog:         int   = 0
        self.outstanding_qty: int   = 0        # quantity on order (if any)

        # --- event queue (min-heap) ---
        self.event_queue: list = []

        # --- statistics ---
        self.stats = SimStats()

        # --- trace log (one row per event) ---
        self.trace: list[dict] = []

        # --- inventory history for plotting ---
        self.history_times:  list[float] = [0.0]
        self.history_levels: list[int]   = [S]

    # ------------------------------------------------------------------
    # 4a.  Random variate generators
    # ------------------------------------------------------------------

    def _next_demand_arrival(self) -> float:
        """Inter-arrival time ~ Exponential(mean = mean_iat)."""
        return self.rng.exponential(self.mean_iat)

    def _demand_size(self) -> int:
        """Demand quantity drawn from the discrete empirical distribution."""
        return int(self.rng.choice(DEMAND_SIZES, p=DEMAND_PROBS))

    def _lead_time(self) -> float:
        """Lead time ~ Uniform(0.5, 1.0) months."""
        return self.rng.uniform(0.5, 1.0)

    # ------------------------------------------------------------------
    # 4b.  Event scheduling helpers
    # ------------------------------------------------------------------

    def _schedule(self, event: Event):
        """Push an event onto the priority queue."""
        heapq.heappush(self.event_queue, event)

    def _next_event(self) -> Event:
        """Pop and return the earliest event."""
        return heapq.heappop(self.event_queue)

    # ------------------------------------------------------------------
    # 4c.  Cost accumulation
    # ------------------------------------------------------------------

    def _accumulate_costs(self, dt: float):
        """
        Update time-weighted holding and shortage integrals.

        Called *before* the state changes at each event.

        Parameters
        ----------
        dt : elapsed time since last event
        """
        pos_inv = max(self.inventory, 0)
        self.stats.inventory_area += pos_inv * dt
        self.stats.backlog_area   += self.backlog * dt
        self.stats.total_holding_cost  += self.h * pos_inv * dt
        self.stats.total_shortage_cost += self.p * self.backlog * dt

    # ------------------------------------------------------------------
    # 4d.  Event handlers
    # ------------------------------------------------------------------

    def _handle_demand(self, event: Event):
        """
        Process a customer demand arrival.

        - Draw demand size d.
        - Decrease inventory by d.  If inventory goes negative the
          deficit becomes (additional) backlog.
        - Schedule the next demand arrival.
        """
        d = self._demand_size()
        self.stats.total_demand += d

        if self.inventory >= d:
            self.inventory -= d
            self.stats.demand_satisfied += d
        else:
            # partially satisfy from stock, rest is backordered
            satisfied = max(self.inventory, 0)
            self.stats.demand_satisfied += satisfied
            shortfall  = d - satisfied
            self.inventory -= d           # inventory becomes negative
            self.backlog   += shortfall   # track absolute backlog separately

        # schedule next demand
        next_arr = self.clock + self._next_demand_arrival()
        if next_arr < self.n_months:
            self._schedule(Event(time=next_arr, event_type=EVENT_DEMAND))

        return d

    def _handle_review(self):
        """
        Monthly inventory review – apply (s, S) policy.

        If inventory position I < s, place an order for (S − I) units.
        The 'inventory position' here is current inventory (which may be
        negative due to backlog).
        """
        order_qty     = 0
        order_arrival = None
        ordering_cost = 0.0

        I = self.inventory   # negative if backlogged

        if I < self.s and self.outstanding_qty == 0:
            order_qty = self.S - I
            ordering_cost = self.K + self.c * order_qty
            self.stats.total_ordering_cost += ordering_cost
            self.stats.num_orders          += 1
            self.outstanding_qty            = order_qty

            lt = self._lead_time()
            order_arrival = self.clock + lt
            self._schedule(Event(time=order_arrival,
                                 event_type=EVENT_ORDER,
                                 order_qty=order_qty))

        # schedule next review (exactly 1 month later, if within horizon)
        next_rev = self.clock + 1.0
        if next_rev <= self.n_months:
            self._schedule(Event(time=next_rev, event_type=EVENT_REVIEW))

        return order_qty, order_arrival, ordering_cost

    def _handle_order_arrival(self, event: Event):
        """
        Process an incoming order.

        1. Clear any outstanding backlog first.
        2. Add remaining units to on-hand inventory.
        """
        qty = event.order_qty
        self.outstanding_qty = 0

        if self.backlog > 0:
            if qty >= self.backlog:
                qty            -= self.backlog
                self.inventory += self.backlog   # clear negative inventory
                self.backlog    = 0
            else:
                self.backlog   -= qty
                self.inventory += qty
                qty             = 0
        else:
            self.inventory += qty

    # ------------------------------------------------------------------
    # 4e.  Initialise and run
    # ------------------------------------------------------------------

    def _initialise(self):
        """Seed the event queue with the first demand arrival and first review."""
        first_demand = self._next_demand_arrival()
        self._schedule(Event(time=first_demand, event_type=EVENT_DEMAND))
        self._schedule(Event(time=1.0, event_type=EVENT_REVIEW))   # month 1 review

    def run(self, verbose: bool = True):
        """
        Execute the simulation.

        Parameters
        ----------
        verbose : if True, print a formatted event trace table to stdout.
        """
        self._initialise()

        if verbose:
            _print_header()

        prev_clock = 0.0

        while self.event_queue:
            event = self._next_event()

            if event.time > self.n_months:
                break                       # past simulation horizon

            # --- accumulate holding / shortage costs for elapsed interval ---
            dt = event.time - prev_clock
            self._accumulate_costs(dt)
            prev_clock   = event.time
            self.clock   = event.time

            # --- dispatch to appropriate handler ---
            demand      = 0
            order_qty   = 0
            order_arr   = None
            order_cost  = 0.0

            if event.event_type == EVENT_DEMAND:
                demand = self._handle_demand(event)

            elif event.event_type == EVENT_REVIEW:
                order_qty, order_arr, order_cost = self._handle_review()

            elif event.event_type == EVENT_ORDER:
                self._handle_order_arrival(event)

            # --- record history for plot ---
            self.history_times.append(self.clock)
            self.history_levels.append(self.inventory)

            # --- build trace row ---
            row = {
                "time":       self.clock,
                "event":      event.event_type,
                "demand":     demand,
                "inventory":  self.inventory,
                "backlog":    self.backlog,
                "order_qty":  order_qty,
                "order_arr":  order_arr,
                "order_cost": order_cost,
                "hold_cost":  self.h * max(self.inventory, 0) * dt,
                "short_cost": self.p * self.backlog * dt,
            }
            self.trace.append(row)

            if verbose:
                _print_row(row)

        # --- final cost accumulation until end of horizon ---
        dt = self.n_months - prev_clock
        self._accumulate_costs(dt)

        if verbose:
            _print_footer()

    # ------------------------------------------------------------------
    # 4f.  Summary statistics
    # ------------------------------------------------------------------

    def summary(self) -> dict:
        """
        Compute and return a dict of summary statistics.

        Returns
        -------
        dict with keys:
            total_ordering_cost, total_holding_cost, total_shortage_cost,
            total_cost, num_orders, avg_inventory, avg_backlog,
            service_level, fill_rate
        """
        total_cost    = (self.stats.total_ordering_cost
                         + self.stats.total_holding_cost
                         + self.stats.total_shortage_cost)
        avg_inventory = self.stats.inventory_area / self.n_months
        avg_backlog   = self.stats.backlog_area   / self.n_months
        service_level = (self.stats.demand_satisfied /
                         self.stats.total_demand) if self.stats.total_demand else 0.0
        fill_rate     = service_level   # for lost-sales it differs; here = CSL approximation

        return {
            "total_ordering_cost": self.stats.total_ordering_cost,
            "total_holding_cost":  self.stats.total_holding_cost,
            "total_shortage_cost": self.stats.total_shortage_cost,
            "total_cost":          total_cost,
            "num_orders":          self.stats.num_orders,
            "avg_inventory":       avg_inventory,
            "avg_backlog":         avg_backlog,
            "service_level":       service_level,
            "fill_rate":           fill_rate,
        }

    def print_summary(self):
        """Pretty-print the summary statistics."""
        s = self.summary()
        bar = "=" * 50
        print(f"\n{bar}")
        print("         SIMULATION SUMMARY")
        print(bar)
        print(f"  Total Ordering Cost  : ${s['total_ordering_cost']:>10.2f}")
        print(f"  Total Holding Cost   : ${s['total_holding_cost']:>10.2f}")
        print(f"  Total Shortage Cost  : ${s['total_shortage_cost']:>10.2f}")
        print(f"  ─────────────────────────────────────")
        print(f"  Total Inventory Cost : ${s['total_cost']:>10.2f}")
        print(f"  Number of Orders     : {s['num_orders']:>11d}")
        print(f"  Average Inventory    : {s['avg_inventory']:>11.3f} units")
        print(f"  Average Backlog      : {s['avg_backlog']:>11.3f} units")
        print(f"  Service Level (CSL)  : {s['service_level']:>10.1%}")
        print(f"  Fill Rate            : {s['fill_rate']:>10.1%}")
        print(bar)

    # ------------------------------------------------------------------
    # 4g.  Plotting
    # ------------------------------------------------------------------

    def plot(self, save_path: Optional[str] = None):
        """
        Plot inventory level vs. time.

        Parameters
        ----------
        save_path : if given, save the figure to this file path.
        """
        fig, ax = plt.subplots(figsize=(14, 5))

        # step plot of inventory level
        ax.step(self.history_times, self.history_levels,
                where="post", color="#2563EB", linewidth=1.4, label="Inventory level")

        # reference lines
        ax.axhline(self.s, color="#DC2626", linewidth=1.2,
                   linestyle="--", label=f"Reorder point  s = {self.s}")
        ax.axhline(self.S, color="#16A34A", linewidth=1.2,
                   linestyle=":",  label=f"Order-up-to   S = {self.S}")
        ax.axhline(0,      color="black",   linewidth=0.8, linestyle="-")

        # shade backlog region
        levels = np.array(self.history_levels)
        times  = np.array(self.history_times)
        ax.fill_between(times, levels, 0,
                        where=(levels < 0),
                        step="post",
                        color="#FCA5A5", alpha=0.5, label="Backlog")

        ax.set_xlabel("Time (months)", fontsize=12)
        ax.set_ylabel("Inventory Level (units)", fontsize=12)
        ax.set_title(f"(s, S) = ({self.s}, {self.S})  Inventory Simulation "
                     f"over {self.n_months} months", fontsize=13, fontweight="bold")
        ax.legend(loc="upper right", fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"\n  Plot saved to: {save_path}")
        plt.show()


# ---------------------------------------------------------------------------
# 5.  Console formatting helpers
# ---------------------------------------------------------------------------

_COL_W = [8, 18, 7, 10, 8, 10, 13, 10, 10, 10]
_HEADERS = [
    "Time", "Event", "Demand", "Inventory",
    "Backlog", "OrderQty", "OrderArrival",
    "OrderCost", "HoldCost", "ShortCost",
]


def _print_header():
    """Print the trace table header."""
    row = "  ".join(h.ljust(_COL_W[i]) for i, h in enumerate(_HEADERS))
    sep = "  ".join("-" * w for w in _COL_W)
    print("\n" + sep)
    print(row)
    print(sep)


def _print_row(r: dict):
    """Print one formatted trace row."""
    arr = f"{r['order_arr']:.4f}" if r["order_arr"] is not None else "—"
    vals = [
        f"{r['time']:.4f}",
        r["event"],
        str(r["demand"])   if r["demand"]    else "—",
        str(r["inventory"]),
        str(r["backlog"])  if r["backlog"]   else "—",
        str(r["order_qty"]) if r["order_qty"] else "—",
        arr,
        f"${r['order_cost']:.2f}" if r["order_cost"] else "—",
        f"${r['hold_cost']:.4f}",
        f"${r['short_cost']:.4f}",
    ]
    print("  ".join(v.ljust(_COL_W[i]) for i, v in enumerate(vals)))


def _print_footer():
    sep = "  ".join("-" * w for w in _COL_W)
    print(sep)


# ---------------------------------------------------------------------------
# 6.  Main entry point
# ---------------------------------------------------------------------------

def get_user_inputs() -> dict:
    """
    Prompt the user for simulation parameters.

    Returns
    -------
    dict of parameter values
    """
    print("=" * 55)
    print("     (s, S) Inventory Simulation – Parameter Setup")
    print("=" * 55)

    def _ask(prompt, cast, default):
        raw = input(f"  {prompt} [{default}]: ").strip()
        return cast(raw) if raw else default

    s        = _ask("Reorder point  s",                  int,   20)
    S        = _ask("Order-up-to level  S",              int,   60)
    n_months = _ask("Simulation horizon (months)",       int,   12)
    h        = _ask("Holding cost h ($/unit/month)",     float, 1.0)
    p        = _ask("Shortage cost p ($/unit/month)",    float, 5.0)
    K        = _ask("Setup cost K ($)",                  float, 32.0)
    c        = _ask("Unit ordering cost c ($/unit)",     float, 3.0)
    seed     = _ask("Random seed (blank = random)",      int,   42)
    verbose  = _ask("Show event trace? (1=yes / 0=no)", int,    1)

    return dict(s=s, S=S, n_months=n_months, h=h, p=p,
                K=K, c=c, seed=seed, verbose=bool(verbose))


def main():
    """Run the (s, S) inventory simulation."""
    params = get_user_inputs()

    print(f"\n  Running {params['n_months']}-month simulation …\n")

    sim = InventorySystem(
        s         = params["s"],
        S         = params["S"],
        n_months  = params["n_months"],
        h         = params["h"],
        p         = params["p"],
        K         = params["K"],
        c         = params["c"],
        mean_iat  = 0.1,            # fixed per requirements
        rng_seed  = params["seed"],
    )

    sim.run(verbose=params["verbose"])
    sim.print_summary()
    sim.plot(save_path="inventory_plot.png")


if __name__ == "__main__":
    main()
