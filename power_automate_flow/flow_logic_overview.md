# Power Automate Flow: Get Candidate Count

This flow acts as the bridge between the AI agent and the data warehouse.

1.  **Trigger**: Receives the 'Diagnosis' (as text) from Copilot Studio.
2.  **Execute SQL Query**: Connects to the Fabric SQL endpoint and runs a parameterized SQL query to find all records in the `dbo.eligiblecandidates` table where the `Conditions` column contains the diagnosis text.
3.  **Compose**: Counts the number of rows returned by the SQL query.
4.  **Respond**: Sends the final count (as a number) back to Copilot Studio.
