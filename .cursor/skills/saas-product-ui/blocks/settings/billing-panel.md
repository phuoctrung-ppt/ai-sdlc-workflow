---
name: billing-panel
category: settings
dial_compatibility:
  variance: [2, 5]
  motion: [1, 3]
  density: [5, 7]
when_to_use: "In-app billing: current plan, payment method, invoices — not public pricing marketing page."
not_for: "Public pricing page with annual toggle spectacle (taste-design / marketing track)."
stack: [react, next, tailwind]
---

# Billing Panel

## Visual sketch

```
┌─ Current plan ─────────────────────────────────────┐
│ Pro · $49/mo                    [Manage plan]      │
│ Renews 12 Sep 2026 · Seat 4/10                     │
└────────────────────────────────────────────────────┘
┌─ Payment method ───────────────────────────────────┐
│ Visa •••• 4242                      [Update]       │
└────────────────────────────────────────────────────┘
┌─ Invoices ─────────────────────────────────────────┐
│ Date       Amount     Status     Receipt           │
│ 01 Aug     $49.00     Paid       Download          │
└────────────────────────────────────────────────────┘
```

## Props API

```ts
type Invoice = {
  id: string;
  date: string;
  amount: string;
  status: "paid" | "open" | "void";
  receiptUrl?: string;
};

type BillingPanelProps = {
  planName: string;
  priceLabel: string; // "$49/mo"
  renewLabel?: string;
  usageLabel?: string; // "4/10 seats"
  onManagePlan?: () => void;
  paymentMethodLabel?: string;
  onUpdatePayment?: () => void;
  invoices: Invoice[];
};
```

## Code sketch

```tsx
import { StatusBadge } from "../data/status-badge"; // conceptual path

export function BillingPanel({
  planName,
  priceLabel,
  renewLabel,
  usageLabel,
  onManagePlan,
  paymentMethodLabel,
  onUpdatePayment,
  invoices,
}: BillingPanelProps) {
  return (
    <div className="mx-auto max-w-xl space-y-6">
      <section className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-[12px] text-zinc-500">Current plan</div>
            <div className="mt-1 text-[15px] font-semibold text-zinc-900 dark:text-zinc-50">
              {planName}{" "}
              <span className="font-normal text-zinc-500">{priceLabel}</span>
            </div>
            {(renewLabel || usageLabel) && (
              <p className="mt-1 text-[12px] text-zinc-500">
                {[renewLabel, usageLabel].filter(Boolean).join(" · ")}
              </p>
            )}
          </div>
          {onManagePlan && (
            <button type="button" onClick={onManagePlan} className="h-8 shrink-0 rounded-md border border-zinc-200 px-3 text-[13px] dark:border-zinc-700">
              Manage plan
            </button>
          )}
        </div>
      </section>

      {paymentMethodLabel && (
        <section className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <div className="flex items-center justify-between gap-3">
            <div>
              <div className="text-[12px] text-zinc-500">Payment method</div>
              <div className="mt-1 text-[13px] text-zinc-900 dark:text-zinc-50">{paymentMethodLabel}</div>
            </div>
            {onUpdatePayment && (
              <button type="button" onClick={onUpdatePayment} className="h-8 rounded-md border border-zinc-200 px-3 text-[13px] dark:border-zinc-700">
                Update
              </button>
            )}
          </div>
        </section>
      )}

      <section>
        <h2 className="mb-2 text-[13px] font-medium text-zinc-900 dark:text-zinc-50">Invoices</h2>
        <div className="overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800">
          <table className="w-full text-left text-[13px]">
            <thead className="bg-zinc-50 text-[12px] text-zinc-500 dark:bg-zinc-900">
              <tr>
                <th className="px-3 py-2 font-medium">Date</th>
                <th className="px-3 py-2 font-medium text-right">Amount</th>
                <th className="px-3 py-2 font-medium">Status</th>
                <th className="px-3 py-2 font-medium" />
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv) => (
                <tr key={inv.id} className="border-t border-zinc-100 dark:border-zinc-900">
                  <td className="px-3 py-2 tabular-nums text-zinc-700 dark:text-zinc-300">{inv.date}</td>
                  <td className="px-3 py-2 text-right tabular-nums">{inv.amount}</td>
                  <td className="px-3 py-2">
                    <StatusBadge
                      label={inv.status}
                      tone={inv.status === "paid" ? "success" : inv.status === "open" ? "warning" : "neutral"}
                    />
                  </td>
                  <td className="px-3 py-2 text-right">
                    {inv.receiptUrl && (
                      <a href={inv.receiptUrl} className="text-[12px] text-zinc-600 underline dark:text-zinc-400">
                        Download
                      </a>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
```

## Mobile fallback

Stack sections; invoice table may scroll-x or simplify to list rows.

## Motion variants

None.

## Dark-mode notes

Cards use elevated surface; invoice header muted.

## Anti-patterns

- Marketing pricing toggle (monthly/yearly spectacle) inside settings
- Hiding next renewal date
- Accent gradients on plan card

## References

- In-app billing examples: plan summary + payment + invoices (SaaS billing UIs 2026)
