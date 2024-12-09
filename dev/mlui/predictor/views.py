# mlui/predictor/views.py
import pickle
import os
import pandas as pd
import logging
from django.shortcuts import render
from django.conf import settings
from .forms import SinglePredictionForm, FileUploadForm
from .models import Prediction

logger = logging.getLogger(__name__)

def load_model():
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(project_root, 'model', 'best_lr_model.pkl')
        
        print(f"Loading model from: {model_path}")
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at: {model_path}")
            return None
            
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Verify model has predict method
        if not hasattr(model, 'predict'):
            logger.error("Loaded object is not a valid model")
            return None
            
        return model
            
    except Exception as e:
        logger.error(f"Model loading error: {e}")
        return None

def save_prediction(features, prediction):
    try:
        print(f"Saving prediction: {prediction} with features: {features}")  # Debug print
        Prediction.objects.create(
            prediction=prediction,
            region=features['region'],
            tenure=features['tenure'],
            age=features['age'],
            marital=features['marital'],
            address=features['address'],
            income=features['income'],
            ed=features['ed'],
            employ=features['employ'],
            retire=features['retire'],
            gender=features['gender'],
            reside=features['reside']
        )
        print("Prediction saved successfully")  # Debug print
        return True
    except Exception as e:
        logger.error(f"Database error: {e}")
        print(f"Database error details: {str(e)}")  # Debug print
        return False


def predict_single(request):
    try:
        if request.method == 'POST':
            form = SinglePredictionForm(request.POST)
            if form.is_valid():
                model = load_model()
                if not model:
                    return render(request, 'predictor/single.html', 
                                {'form': form, 'error': "Could not load model"})
                
                features = ['region', 'tenure', 'age', 'marital', 'address', 
                          'income', 'ed', 'employ', 'retire', 'gender', 'reside']
                data = [[form.cleaned_data[f] for f in features]]
                
                try:
                    prediction = model.predict(data)[0]
                    if save_prediction(form.cleaned_data, prediction):
                        return render(request, 'predictor/result.html', 
                                    {
                                        'prediction': prediction, 
                                        'features': form.cleaned_data,
                                        'success_message': f"Prediction saved successfully! Category: {prediction}"
                                    })
                    else:
                        return render(request, 'predictor/single.html', 
                                    {'form': form, 'error': "Could not save prediction to database"})
                except Exception as e:
                    logger.error(f"Prediction error: {e}")
                    return render(request, 'predictor/single.html', 
                                {'form': form, 'error': f"Prediction failed: {str(e)}"})
        else:
            form = SinglePredictionForm()
        return render(request, 'predictor/single.html', {'form': form})
    except Exception as e:
        logger.error(f"View error: {e}")
        return render(request, 'predictor/single.html', 
                     {'form': SinglePredictionForm(), 'error': f"An error occurred: {str(e)}"})


def predict_file(request):
    try:
        if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                model = load_model()
                if not model:
                    return render(request, 'predictor/file.html', 
                                {'form': form, 'error': "Could not load model"})
                
                try:
                    df = pd.read_csv(request.FILES['file'])
                    required_columns = ['region', 'tenure', 'age', 'marital', 'address', 
                                      'income', 'ed', 'employ', 'retire', 'gender', 'reside']
                    
                    if not all(col in df.columns for col in required_columns):
                        return render(request, 'predictor/file.html', 
                                    {'form': form, 'error': "Invalid file format"})
                    
                    predictions = model.predict(df[required_columns])
                    results = []
                    
                    # Save each prediction
                    for i, row in df.iterrows():
                        features = row[required_columns].to_dict()
                        if save_prediction(features, predictions[i]):
                            results.append((features, predictions[i]))
                    
                    return render(request, 'predictor/result.html', 
                                {'predictions': results})
                except Exception as e:
                    logger.error(f"File processing error: {e}")
                    return render(request, 'predictor/file.html', 
                                {'form': form, 'error': "File processing failed"})
        else:
            form = FileUploadForm()
        return render(request, 'predictor/file.html', {'form': form})
    except Exception as e:
        logger.error(f"View error: {e}")
        return render(request, 'predictor/file.html', 
                     {'form': FileUploadForm(), 'error': "An error occurred"})