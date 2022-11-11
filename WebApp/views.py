from ast import literal_eval

import joblib
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

ku_model_prediction_ubl = None


@csrf_exempt
def score_prediction_ubl(request):
    global ku_model_prediction_ubl
    if request.method == 'POST':
        if ku_model_prediction_ubl is None:
            ku_model_prediction_ubl = joblib.load("ai_models/ku_model_prediction_ubl.sav")
        list_of_list_data = request.POST.get('student_data[[]]', None)
        # parse list of list data string
        try:
            list_of_list_data = literal_eval(list_of_list_data)
            if (list_of_list_data == [[]]):
                return JsonResponse([], safe=False)
            assert isinstance(list_of_list_data[0], list) #2d list
            assert all(len(e) == 5 for e in list_of_list_data)
        except:
            return HttpResponse('Please send "student_data[[]]" in correct format, eg. [[1,2,3,4,5]]', status=422)

        outcome = ku_model_prediction_ubl.predict(list_of_list_data)
        return JsonResponse(list(outcome), safe=False)
    else:
        return HttpResponse('Not allowed', status=201)
