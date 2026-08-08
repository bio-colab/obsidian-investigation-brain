# EV-XFER-001: Bank transfer graph among shells

type_hint: financial-record  
source_kind: operational  

## Content (desensitized training excerpt)

Bank compliance export (training numbers):

| Date | From | To | Amount (USD) | Memo |
|------|------|-----|--------------|------|
| 2018-03-02 | Pier Grocery operating | Dockside Consult LLC | 2,500 | "consulting" |
| 2018-03-05 | Dockside Consult LLC | North Current Billing LLC | 2,200 | internal |
| 2018-03-06 | North Current Billing LLC | HHG Parent LLC | 2,000 | management fee |
| 2018-04-02 | Pier Grocery operating | Dockside Consult LLC | 2,500 | "consulting" |

Pattern: funds cascade shell → shell → parent within days of grocery payments.

## Limits
- No proof of duress in the bank file itself.
- No other merchants' payments included in this packet.

## Notes for vault
- financial-record + CoC.
- Use in Enterprise-Map financial-edges.
- Counter remains: legitimate consulting invoices (invoices themselves **not** in packet).
