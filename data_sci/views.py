from django.shortcuts import render, redirect
from django.http import HttpResponse

from data_sci.models import PimaIndianDiabetic, PersonalHealthProfile
from django.core.paginator import Paginator

import pandas as pd
import pickle

def import_diabetic_data_csv(request):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQN9e5B883gr07NHT0oVWj5Q3d8jE01CqWTcOG_piq_UH2PZKgEjJzwTfj5LrinpEi8TQml2zRhyH3x/pub?output=csv'
    df = pd.read_csv(csv_url)
    print(f"Total records in CSV: {df.shape[0]}") 
    
    if df.empty:
        print("No data found in the CSV.")
        return render(request, 'data_sci/pima_indian_data.html', {'error': 'No data found in the CSV.'})
    
    instances = [
        PimaIndianDiabetic(
            Pregnancies=float(row['Pregnancies']),
            Glucose=float(row['Glucose']),
            BloodPressure=float(row['BloodPressure']),
            SkinThickness=float(row['SkinThickness']),
            Insulin=float(row['Insulin']),
            BMI=float(row['BMI']),
            DiabetesPedigreeFunction=float(row['DiabetesPedigreeFunction']),
            Age=float(row['Age']),
            Outcome=int(row['Outcome']),
        )
        for _ , row in df.iterrows()
    ]

    PimaIndianDiabetic.objects.bulk_create(instances, ignore_conflicts=True)  # Using `ignore_conflicts` to skip duplicates

    all_instances = PimaIndianDiabetic.objects.all().order_by('id')
    paginator = Paginator(all_instances, 25) 
    page_number = request.GET.get('page', 1)
    success_instances = paginator.get_page(page_number)

    context = {
        'success_instances': success_instances,
    }

    return render(request, 'data_sci/pima_indian_data.html', context)

def personal_health_data_list(request):
    dataset_objs = PersonalHealthProfile.objects.all()
    context_data = {
        "filter_type": "All",
        "datasets": dataset_objs,
    }

    return render(request, 'data_sci/personal_health_data.html', context_data)

def predict_diabetic_instance(input_data):
    model_path = f'/workspaces/MultiDiabeticWebsite/voting_SVMXGBLGBM.pkl'
    
    with open(model_path, 'rb') as file:
        final_model = pickle.load(file)
    y_pred = final_model.predict(input_data)
    
    return y_pred

def personal_health_data_add(request):
    if request.method == "POST":
        form_data = request.POST
        pregnancies = form_data['pregnancies']
        glucose = form_data['glucose']
        insulin = form_data['insulin']
        bmi = form_data['bmi']
        age = form_data['age']

        input_data = [
            [
                float(pregnancies), 
                float(glucose), 
                float(insulin), 
                float(bmi), 
                float(age)
            ]
        ]

        y_pred = predict_diabetic_instance(input_data)
        prediction = int(y_pred[0])
        result_message = 'Diabetes' if prediction == 1 else 'No Diabetes'

        new_item = PersonalHealthProfile(
            Pregnancies = pregnancies,
            Glucose = glucose,
            Insulin = insulin,
            BMI = bmi,
            Age = age,
            Prediction = result_message,
        )

        try:
            new_item.save()
        except:
            return HttpResponse("ERROR!")
        
        return redirect('personal_health_list')

    return render(request, 'data_sci/diabetic_prediction.html')

def personal_health_data_edit(request, id):
    try:
        item = PersonalHealthProfile.objects.get(id = id)
    except PersonalHealthProfile.DoesNotExist:
        return HttpResponse("ID Not found", status=404)
    
    if request.method == "POST":
        print('Editing')
        form_data = request.POST

        try:
            input_data = [
                [
                    float(form_data['pregnancies']), 
                    float(form_data['glucose']), 
                    float(form_data['insulin']), 
                    float(form_data['bmi']), 
                    float(form_data['age'])
                ]
            ]
        except ValueError:
            return HttpResponse("Invalid input data", status=400)

        y_pred = predict_diabetic_instance(input_data)
        prediction = int(y_pred[0])
        result_message = 'Diabetes' if prediction == 1 else 'No Diabetes'

        item.Pregnancies = form_data['pregnancies']
        item.Glucose = form_data['glucose']
        item.Insulin = form_data['insulin']
        item.BMI = form_data['bmi']
        item.Age = form_data['age']
        item.Prediction = result_message

        try:
            item.save()
        except  Exception as e:
            return HttpResponse("ERROR! Edit the instance")

        return redirect('personal_health_list')
    
    else:
        context_data = {
            'item_id': id,
            'form_data': {
                'pregnancies': item.Pregnancies,
                'glucose': item.Glucose,
                'insulin': item.Insulin, 
                'bmi': item.BMI,
                'age': item.Age,

            }
        }

        return render(request, 'data_sci/diabetic_prediction.html', context=context_data)
 
def personal_health_data_delete(request, id):
    dataset_objs = PersonalHealthProfile.objects.filter(id = id)
    if len(dataset_objs) <= 0:
        return HttpResponse("ID Not Found")
    dataset_objs.delete()
    
    return redirect('personal_health_list')

def personal_dashboard(request):
    return render(request, 'data_sci/personal_dashboard.html')