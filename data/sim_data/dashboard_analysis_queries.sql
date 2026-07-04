-- Dashboard analysis queries for simulated teacher assistant data
-- Target database: data/sim_data/teacher_assistant_simulated_data.sqlite

-- 1) Student 360 view (one student, one course)
SELECT
  s.student_id,
  s.first_name,
  s.last_name,
  c.course_name,
  gs.current_grade_pct,
  gs.risk_band,
  gs.missing_assignments,
  gs.absences,
  gs.tardies,
  gs.behavior_incidents
FROM students s
JOIN enrollments e
  ON e.student_id = s.student_id
JOIN courses c
  ON c.course_id = e.course_id
LEFT JOIN grade_snapshots gs
  ON gs.student_id = s.student_id
 AND gs.course_id = c.course_id;


-- 2) Attendance-risk correlation
SELECT
  gs.course_id,
  gs.risk_band,
  AVG(gs.absences) AS avg_absences,
  AVG(gs.tardies) AS avg_tardies,
  AVG(gs.current_grade_pct) AS avg_grade
FROM grade_snapshots gs
GROUP BY gs.course_id, gs.risk_band
ORDER BY gs.course_id, gs.risk_band;


-- 3) Assignment performance with missing/late pressure
SELECT
  sc.course_id,
  a.unit,
  a.assignment_type,
  COUNT(*) AS submissions,
  SUM(CASE WHEN sc.missing_flag = 'Yes' THEN 1 ELSE 0 END) AS missing_count,
  SUM(CASE WHEN sc.late_flag = 'Yes' THEN 1 ELSE 0 END) AS late_count,
  AVG(CASE
        WHEN sc.points_possible > 0
        THEN 100.0 * sc.points_earned / sc.points_possible
      END) AS avg_pct
FROM assignment_scores sc
JOIN assignments a
  ON a.assignment_id = sc.assignment_id
GROUP BY sc.course_id, a.unit, a.assignment_type
ORDER BY sc.course_id, a.unit;


-- 4) Intervention impact snapshot (descriptive)
SELECT
  i.intervention_type,
  COUNT(*) AS interventions,
  AVG(gs.current_grade_pct) AS avg_grade_at_snapshot,
  AVG(gs.missing_assignments) AS avg_missing_at_snapshot,
  AVG(gs.absences) AS avg_absences_at_snapshot
FROM interventions i
JOIN grade_snapshots gs
  ON gs.student_id = i.student_id
 AND gs.course_id = i.course_id
GROUP BY i.intervention_type
ORDER BY interventions DESC;


-- 5) Behavior + outcomes
SELECT
  gs.risk_band,
  COUNT(DISTINCT bi.student_id) AS students_with_incidents,
  AVG(gs.current_grade_pct) AS avg_grade
FROM grade_snapshots gs
LEFT JOIN behavior_incidents bi
  ON bi.student_id = gs.student_id
 AND bi.course_id = gs.course_id
GROUP BY gs.risk_band
ORDER BY gs.risk_band;
