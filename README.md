# APS_Fault_Dectection:
The Air Pressure System (APS) is a crucial component in heavy-duty vehicles, responsible for generating and regulating compressed air for various operations, including braking and gear changes. This is a machine learning model that predicts APS failures using real-time sensor data from browsers.
This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

# Solution Proposed:
In this project, the system in focus is the Air Pressure System (APS), which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to APS system.
The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

Data: Sensor Data
Cost Consideration in Predictions:
Cost_1: The expense of unnecessary maintenance checks due to false positives.
Cost_2: The expense of missing a faulty truck due to false negatives, leading to potential breakdowns.

Total Cost Calculation:
Total_cost = Cost_1 × No_Instances + Cost_2 × No_Instances
Cost_1: Cost of an unnecessary checkup at a workshop (false positive).
Cost_2: Cost of missing a faulty truck, leading to a breakdown (false negative).

False Negatives Are More Costly:
The cost of a false negative is 50 times higher than a false positive.
The focus should be on minimizing false negatives while also reducing false positives.

