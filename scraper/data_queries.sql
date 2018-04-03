--Lookup for which game_ids are for games with a particular player in them
SELECT DISTINCT
    game_id,
    val as player
FROM stats_games
WHERE attribute like 'player%'
;

--See winrate for one player
SELECT
    attr
    ,COUNT(*) as games
    ,SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) as wins
    ,(SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) * 1.0) / (COUNT(*) * 1.0) as win_rate
FROM stats_Game games
INNER JOIN  stats_GamePlayerRelationship pg_lkup on
    pg_lkup.game_id = games.game_id and
    pg_lkup.player_name = 'diggs' and
    games.attr = 'game_outcome'
GROUP BY attr
;

--Compare win rate with / without another player

--Compare win rates for one player with other players (on an individual basis)

--Compare win rates for one player with other players (on a team basis)

--Compare number of games player with / without another player

--See number of ranked/unranked games tracked
