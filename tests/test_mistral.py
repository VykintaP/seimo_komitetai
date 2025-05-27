from ml_pipeline.mistral_classifier import classify_with_mistral

test_question = "Dėl valstybinės vaistų kainodaros sistemos keitimo"
predicted_topic = classify_with_mistral(test_question)

print(f"Question: {test_question}")
print(f"Predicted topic: {predicted_topic}")
