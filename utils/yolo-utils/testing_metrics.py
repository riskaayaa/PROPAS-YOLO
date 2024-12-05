import geopandas as gpd
from shapely.geometry import shape

# Load the GeoJSON data
generated_data = gpd.read_file("public/patch-temp/bogor52-test-ref.geojson")
actual_data = gpd.read_file("public/patch-temp/digit-bogor.geojson")

# # Function to calculate true positives (TP), false positives (FP), and false negatives (FN)
# def calculate_tp_fp_fn(generated_data, actual_data):
#     true_positive = 0
#     false_positive = 0
#     false_negative = 0

#     # Iterate through each feature in the generated data
#     for index, row in generated_data.iterrows():
#         generated_geometry = shape(row['geometry'])
        
#         # Check if the generated geometry intersects with any actual geometry
#         if actual_data.intersects(generated_geometry).any():
#             true_positive += 1
#         else:
#             false_positive += 1
    
#     # Iterate through each feature in the actual data
#     for index, row in actual_data.iterrows():
#         actual_geometry = shape(row['geometry'])
        
#         # Check if the actual geometry intersects with any generated geometry
#         if not generated_data.intersects(actual_geometry).any():
#             false_negative += 1

#     return true_positive, false_positive, false_negative

# # Calculate true positives (TP), false positives (FP), and false negatives (FN)
# true_positive, false_positive, false_negative = calculate_tp_fp_fn(generated_data, actual_data)

# # Calculate metrics using TP, FP, FN
# total_actual_positives = true_positive + false_negative
# accuracy = (true_positive) / (true_positive + false_positive + false_negative) * 100
# precision = true_positive / (true_positive + false_positive) * 100 if (true_positive + false_positive) > 0 else 0
# recall = true_positive / (true_positive + false_negative) * 100 if (true_positive + false_negative) > 0 else 0
# f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# # Format the results to two decimal places
# accuracy = "{:.2f}".format(accuracy)
# precision = "{:.2f}".format(precision)
# recall = "{:.2f}".format(recall)
# f1_score = "{:.2f}".format(f1_score)

# print("Accuracy:", accuracy, "%")
# print("Precision:", precision, "%")
# print("Recall:", recall, "%")
# print("F1 Score:", f1_score, "%")

# print("True Positives (TP):", true_positive)
# print("False Negatives (FN):", false_negative)
# print("False Positives (FP):", false_positive)


# Function to calculate true positives (TP), false positives (FP), false negatives (FN), omission, and commission
def calculate_metrics(generated_data, actual_data):
    true_positive = 0
    false_positive = 0
    false_negative = 0

    # Iterate through each feature in the generated data
    for index, row in generated_data.iterrows():
        generated_geometry = shape(row['geometry'])
        
        # Check if the generated geometry intersects with any actual geometry
        if actual_data.intersects(generated_geometry).any():
            true_positive += 1
        else:
            false_positive += 1
    
    # Iterate through each feature in the actual data
    for index, row in actual_data.iterrows():
        actual_geometry = shape(row['geometry'])
        
        # Check if the actual geometry intersects with any generated geometry
        if not generated_data.intersects(actual_geometry).any():
            false_negative += 1

    # Calculate omission and commission
    # total_negative = len(generated_data) - true_positive
    omission = false_negative / (false_negative + true_positive) * 100
    commission = false_positive / (false_positive + true_positive) * 100

    return true_positive, false_positive, false_negative, omission, commission

# Calculate metrics including TP, FP, FN, omission, and commission
true_positive, false_positive, false_negative, omission, commission = calculate_metrics(generated_data, actual_data)

# Calculate metrics using TP, FP, FN
total_actual_positives = true_positive + false_negative
accuracy = (true_positive) / (true_positive + false_positive + false_negative) * 100
precision = true_positive / (true_positive + false_positive) * 100 if (true_positive + false_positive) > 0 else 0
recall = true_positive / (true_positive + false_negative) * 100 if (true_positive + false_negative) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Format the results to two decimal places
accuracy = "{:.2f}".format(accuracy)
precision = "{:.2f}".format(precision)
recall = "{:.2f}".format(recall)
f1_score = "{:.2f}".format(f1_score)

print("Accuracy:", accuracy, "%")
print("Precision:", precision, "%")
print("Recall:", recall, "%")
print("F1 Score:", f1_score, "%")

print("True Positives (TP):", true_positive)
print("False Negatives (FN):", false_negative)
print("False Positives (FP):", false_positive)
print("Omission:", "{:.2f}".format(omission), "%")
print("Commission:", "{:.2f}".format(commission), "%")
