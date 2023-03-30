```mermaid
erDiagram
        tournaments ||--o{ tournaments_teams : "participates in"
        countries ||--o{ people : "belongs to"
        people ||--|{ in_game_roles : "plays"
        people ||--o{ people_teams_roles : "part of"
        teams ||--|{ people_teams_roles : "has"
        tournaments ||--|{ groups : "has"
        teams ||--o{ tournaments_teams : "participates in"

```