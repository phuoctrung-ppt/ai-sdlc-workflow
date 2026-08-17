# WCAG 2.2 AA — product web app map

Normative source: https://www.w3.org/TR/WCAG22/ · repo https://github.com/w3c/wcag  
License: W3C Document License (attribution required).

Use this table when implementing or reviewing product UI. Not a full checklist of every criterion.

| Need | Criteria (AA) | Product implication |
|------|---------------|---------------------|
| Keyboard | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11 | All actions keyboard-operable; no traps; logical focus order; visible focus; focus not fully obscured |
| Name / role / value | 4.1.2 | Native controls or correct ARIA; labels programmatically associated |
| Labels & instructions | 1.3.1, 3.3.2 | Visible labels; group related fields |
| Errors | 3.3.1, 3.3.3, 3.3.4 | Identify error; suggest fix; confirm high-risk actions |
| Contrast | 1.4.3, 1.4.11 | Text AA; UI component / graphic contrast |
| Motion | 2.2.2, 2.3.3 | Pause/stop moving content; reduced motion respected |
| Status messages | 4.1.3 | Live regions for toasts/async status without focus steal |
| Target size | 2.5.8 | Pointer targets ≥ 24×24 CSS px (or spacing exception) |
| Consistent nav | 3.2.3, 3.2.4 | Same chrome / same component labels across views |

## Non-goals for this skill

- Full audit methodology (use dedicated a11y tooling)
- AAA criteria unless product policy raises the bar
