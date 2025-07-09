from pyspark.sql.functions import lit, rand, when

# Load tables from your Lakehouse
df_trials = spark.read.table("ClinicalDataHub.TrialCriteria")
df_patients = spark.read.table("ClinicalDataHub.PatientData")

# Clean up column names for the TRIALS dataframe
for col in df_trials.columns:
    df_trials = df_trials.withColumnRenamed(col, col.replace(" ", "_"))

# Clean up column names for the PATIENTS dataframe
for col in df_patients.columns:
    df_patients = df_patients.withColumnRenamed(col, col.replace(" ", "_"))


# Add a mock 'Age' column to the patient data
df_patients = df_patients.withColumn("Age", (rand() * 70 + 15).cast("integer"))

# Create an 'AgeGroup' column based on the mock Age
df_patients = df_patients.withColumn(
    "AgeGroup", when(df_patients.Age >= 18, "ADULT").otherwise("CHILD")
)

# Add a 'Diagnosis' column for matching
df_patients = df_patients.withColumn("Diagnosis", lit("Diabetes"))

# Join the two dataframes using the cleaned-up column names
df_eligible = df_trials.join(
    df_patients,
    (
        (df_patients.AgeGroup == df_trials.Standard_Age)
        & (df_trials.conditions.contains(df_patients.Diagnosis))
    ),
    "inner",
)

# Save the final, combined dataframe as a new "gold" table
df_eligible.write.mode("overwrite").saveAsTable("ClinicalDataHub.EligibleCandidates")

print("Success! The 'EligibleCandidates' table has been created.")

# Optional: Display the results to verify
df_eligible.select(
    "PatientID", "AgeGroup", "Standard_Age", "conditions", "Full_Title"
).show()
