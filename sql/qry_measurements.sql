SELECT 
    measurements.id as measurement_id,
    measurements.sn,
    measurements.created, 
    measurements.machine, 
    measurements.value, 
    features.id as feature_id, 
    features.name as feature_name, 
    features.units, 
    features.lsl, 
    features.usl, 
    notes.note_text
FROM measurements
JOIN features ON features.id = measurements.feature_id
FULL OUTER JOIN notes on notes.measurement_id = measurements.id;
