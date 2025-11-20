(function() {
    // This script runs when it hears the 'sla.predict.trigger' event
    // 'event' is the event object, 'current' is the incident

    gs.log('--- 1. SCRIPT ACTION STARTED for ' + current.number, 'SLA_Predictor');

    try {
        var payload = {};
        payload.priority = current.priority.getDisplayValue();
        payload.category = current.category.getDisplayValue();
        payload.assignment_group = current.assignment_group.getDisplayValue();

        gs.log('--- 2. Payload created (Simple): ' + JSON.stringify(payload), 'SLA_Predictor');

        // --- CHECK THESE TWO LINES ---
        var restMessageName = 'SLA PredictER API';
        var httpMethodName = 'post';
        // -----------------------------

        var r_sync = new sn_ws.RESTMessageV2(restMessageName, httpMethodName);

        if (!r_sync) {
            gs.log('--- 5. SCRIPT ACTION CRASHED: Could not find REST Message "' + restMessageName + '" with method "' + httpMethodName + '".', 'SLA_Predictor');
            return; // Stop the script
        }

        r_sync.setRequestBody(JSON.stringify(payload));

        var response_sync = r_sync.execute();
        var responseBody = response_sync.getBody();
        var httpStatus = response_sync.getStatusCode();

        gs.log('--- 3. API Response Status: ' + httpStatus, 'SLA_Predictor');

        if (httpStatus == 200) {
            var responseObj = JSON.parse(responseBody);
            var prob = parseFloat(responseObj.breach_probability);

            gs.log('--- 4. Probability received: ' + prob, 'SLA_Predictor');

            var grIncident = new GlideRecord('incident');
            if (grIncident.get(current.sys_id)) {

                // Set the probability
                grIncident.setValue('u_sla_breach_probability', prob);

                // Set the risk
                var riskValue = 'low';
                if (prob > 0.7) {
                    riskValue = 'high';
                } else if (prob > 0.3) {
                    riskValue = 'medium';
                }

                grIncident.setValue('u_sla_breach_risk', riskValue);

                grIncident.setWorkflow(false);
                grIncident.autoSysFields(false);
                grIncident.update();

                gs.log('--- 5. Incident ' + current.number + ' updated successfully.', 'SLA_Predictor');

            } else {
                gs.log('--- 5. SCRIPT ACTION FAILED: Could not find incident ' + current.sys_id, 'SLA_Predictor');
            }

        } else {
            gs.log('SLA Predictor API Failed: ' + httpStatus + ' for ' + current.number, 'SLA_Predictor');
        }

    } catch (ex) {
        // This log will catch any crash
        gs.log("--- 99. SCRIPT CRASHED --- " + ex.getMessage(), 'SLA_Predictor');
    }

})();