# Phase 3: Project Design Phase

## Application Architecture
```text
[ User Browser (Jinja2 Template UI) ]
             |
             v  (POST /generate)
     [ FastAPI Backend ]
        /         \
       v           v
 [Image Generator]  [PDF Engine]
  (Fallback Stack)   (ReportLab)
       |               |
       v               v
 [Static/Panels] -> [Export PDF]
