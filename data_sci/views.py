from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.db.models import Count, Avg, Count

from data_sci.models import PimaIndianDiabetic, PersonalHealthProfile
from django.core.paginator import Paginator

import pandas as pd
import pickle

def delete_all_pima_indian_diabetic_records(request):
    all_records = PimaIndianDiabetic.objects.all()
    all_records.delete()
    return JsonResponse({'message': 'All records deleted successfully'})


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

def visualize_pima_diabetic_kaggle_data(request):
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

def determine_glucose_level(glucose):
    if glucose < 100:
        return 'Normal'
    elif 100 <= glucose <= 125:
        return 'Pre-diabetes'
    else:
        return 'Diabetes'

def determine_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        return 'Normal weight'
    elif 25 <= bmi <= 29.9:
        return 'Overweight'
    else:
        return 'Obese'

def health_tracker_data(request):
    averages = PersonalHealthProfile.objects.aggregate(
        average_bmi=Avg('BMI'),
        average_glucose=Avg('Glucose'),
        average_insulin=Avg('Insulin')
    )

    context = {
        'average_bmi': round(averages.get('average_bmi', 0), 2),
        'average_glucose': round(averages.get('average_glucose', 0), 2),
        'average_insulin': round(averages.get('average_insulin', 0), 2),
    }

    return JsonResponse(context, safe=False)

def personal_health_data_add(request):
    last_record = PersonalHealthProfile.objects.latest('added_date')
    context = {
        'last_record': last_record,
        'result_message': None,
        'changes': {
            'pregnancies_change': 0,
            'glucose_change': 0,
            'insulin_change': 0,
            'bmi_change': 0,
            'age_change': 0,
        },
        'glucose_category': None,
        'bmi_category': None,   
    }

    if request.method == "POST":
        form_data = request.POST
        pregnancies = int(form_data.get('pregnancies', 0))
        glucose = float(form_data.get('glucose', 0))
        insulin = float(form_data.get('insulin', 0))
        bmi = float(form_data.get('bmi', 0))
        age = int(form_data.get('age', 0))

        input_data = [[pregnancies, glucose, insulin, bmi, age]]

        y_pred = predict_diabetic_instance(input_data)
        prediction = int(y_pred[0])
        result_message = 'Diabetes' if prediction == 1 else 'No Diabetes'

        changes = {}
        if last_record:
            changes = {
                'pregnancies_change': pregnancies - last_record.Pregnancies,
                'glucose_change': glucose - last_record.Glucose,
                'insulin_change': insulin - last_record.Insulin,
                'bmi_change': bmi - last_record.BMI,
                'age_change': age - last_record.Age,
            }

        new_item = PersonalHealthProfile(
            Pregnancies=pregnancies,
            Glucose=glucose,
            Insulin=insulin,
            BMI=bmi,
            Age=age,
            Prediction=result_message,
        )

        try:
            new_item.save()
            print('Your health data has been recorded successfully!')
        except Exception as e:  
            print(f"ERROR: {e}")
            return redirect('person_dashboard') 

        context['result_message'] = result_message
        context['changes'] = changes

        context['glucose_category'] = determine_glucose_level(glucose)
        context['bmi_category'] = determine_bmi_category(bmi)

        print(f'Get the context: {context}')
        return render(request, 'data_sci/personal_dashboard.html', context)

    print('GET Request')
    return render(request, 'data_sci/personal_dashboard.html', context)

def personal_health_data_add2(request):
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

def scatter_plot_data(request):
    data = list(
        PimaIndianDiabetic.objects.values(
            "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
        ).distinct()
    )
    return JsonResponse(data, safe=False)

def scatter_plot_view(request):
    features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    context = {
        'features': features,
    }
    return render(request, 'data_sci/visualization.html', context)

def diabetic_distribution_data(request):
    total_data_points = PimaIndianDiabetic.objects.count()

    average_bmi = PimaIndianDiabetic.objects.aggregate(Avg('BMI'))['BMI__avg']
    average_glucose = PimaIndianDiabetic.objects.aggregate(Avg('Glucose'))['Glucose__avg']
    average_insulin = PimaIndianDiabetic.objects.aggregate(Avg('Insulin'))['Insulin__avg']

    outcome_counts = PimaIndianDiabetic.objects.values('Outcome').annotate(total=Count('Outcome'))

    data = {
        'non_diabetic': 0,
        'diabetic': 0,
        'average_bmi': round(average_bmi, 2) if average_bmi is not None else 0,
        'average_glucose': round(average_glucose, 2) if average_glucose is not None else 0,
        'average_insulin': round(average_insulin, 2) if average_insulin is not None else 0,
        'total_data_points': total_data_points,
    }

    for entry in outcome_counts:
        if entry['Outcome'] == 1:
            data['diabetic'] = entry['total']
        else:
            data['non_diabetic'] = entry['total']

    return JsonResponse(data, safe=False)

def personal_dashboard(request):
    return render(request, 'data_sci/personal_dashboard.html')

