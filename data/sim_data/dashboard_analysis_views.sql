-- Reusable dashboard views for simulated teacher assistant data
-- Target database: data/sim_data/teacher_assistant_simulated_data.sqlite

DROP VIEW IF EXISTS vw_student_360;
CREATE VIEW vw_student_360 AS
SELECT
  s.student_id,
  s.first_name,
  s.last_name,
  s.preferred_name,
  s.grade_level,
  c.course_id,
  c.course_name,
  c.term,
  c.period,
  gs.week_number,
  gs.current_grade_pct,
  gs.assignment_avg_pct,
  gs.assessment_avg_pct,
  gs.missing_assignments,
  gs.late_assignments,
  gs.absences,
  gs.tardies,
  gs.behavior_incidents,
  gs.risk_band,
  gs.recommended_next_step
FROM students s
JOIN enrollments e
  ON e.student_id = s.student_id
JOIN courses c
  ON c.course_id = e.course_id
LEFT JOIN grade_snapshots gs
  ON gs.student_id = s.student_id
 AND gs.course_id = c.course_id;


DROP VIEW IF EXISTS vw_course_risk_summary;
CREATE VIEW vw_course_risk_summary AS
SELECT
  gs.course_id,
  gs.risk_band,
  COUNT(*) AS student_count,
  AVG(gs.absences) AS avg_absences,
  AVG(gs.tardies) AS avg_tardies,
  AVG(gs.current_grade_pct) AS avg_grade_pct,
  AVG(gs.missing_assignments) AS avg_missing_assignments,
  AVG(gs.late_assignments) AS avg_late_assignments
FROM grade_snapshots gs
GROUP BY gs.course_id, gs.risk_band;


DROP VIEW IF EXISTS vw_assignment_performance;
CREATE VIEW vw_assignment_performance AS
SELECT
  sc.course_id,
  a.unit,
  a.assignment_type,
  COUNT(*) AS submissions,
  SUM(CASE WHEN sc.missing_flag = 'Yes' THEN 1 ELSE 0 END) AS missing_count,
  SUM(CASE WHEN sc.late_flag = 'Yes' THEN 1 ELSE 0 END) AS late_count,
  AVG(
    CASE
      WHEN sc.points_possible > 0
      THEN 100.0 * sc.points_earned / sc.points_possible
      ELSE NULL
    END
  ) AS avg_pct
FROM assignment_scores sc
JOIN assignments a
  ON a.assignment_id = sc.assignment_id
GROUP BY sc.course_id, a.unit, a.assignment_type;


DROP VIEW IF EXISTS vw_intervention_effects;
CREATE VIEW vw_intervention_effects AS
SELECT
  i.intervention_type,
  COUNT(*) AS intervention_count,
  COUNT(DISTINCT i.student_id) AS unique_students,
  AVG(gs.current_grade_pct) AS avg_grade_at_snapshot,
  AVG(gs.missing_assignments) AS avg_missing_at_snapshot,
  AVG(gs.absences) AS avg_absences_at_snapshot,
  AVG(gs.tardies) AS avg_tardies_at_snapshot
FROM interventions i
JOIN grade_snapshots gs
  ON gs.student_id = i.student_id
 AND gs.course_id = i.course_id
GROUP BY i.intervention_type;


DROP VIEW IF EXISTS vw_behavior_outcomes;
CREATE VIEW vw_behavior_outcomes AS
SELECT
  gs.course_id,
  gs.risk_band,
  COUNT(DISTINCT gs.student_id) AS students_in_band,
  COUNT(DISTINCT CASE WHEN bi.student_id IS NOT NULL THEN gs.student_id END) AS students_with_incidents,
  AVG(gs.current_grade_pct) AS avg_grade_pct,
  AVG(gs.behavior_incidents) AS avg_behavior_incidents_snapshot
FROM grade_snapshots gs
LEFT JOIN behavior_incidents bi
  ON bi.student_id = gs.student_id
 AND bi.course_id = gs.course_id
GROUP BY gs.course_id, gs.risk_band;
