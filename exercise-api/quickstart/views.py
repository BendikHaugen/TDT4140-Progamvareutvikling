from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework.parsers import MultiPartParser, FormParser

from .models import CustomUser, Musclegroup, Exercise, Workout, Post, Feedback
from rest_framework import viewsets
from .serializers import UserSerializer, MusclegroupSerializer, ExerciseSerializer, WorkoutSerializer, FeedbackSerializer
from django.views import View
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class GetMeView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        return Response({'username': user.username, 'email': user.email, 'role': user.role})


class MusclegroupViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()

    queryset = Musclegroup.objects.all()
    serializer_class = MusclegroupSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()

    parser_classes = (MultiPartParser, FormParser)

    queryset = Exercise.objects.order_by('-date', '-user__role')
    serializer_class = ExerciseSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()

    parser_classes = (MultiPartParser, FormParser)

    queryset = Workout.objects.order_by('-date', '-user__role')
    serializer_class = WorkoutSerializer


class UserPostsViewSet(APIView):
    permission_classes = ()
    authentication_classes = ()

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(username=request.data['username'])
        exerciseArray = []
        exercises = Exercise.objects.filter(user__username=request.data['username']).order_by('-id')
        for exercise in exercises:
            exerciseArray.append(exercise)
        exerciseSerializer = ExerciseSerializer(exerciseArray, many=True)
        workoutArray = []
        workouts = Workout.objects.filter(user__username=request.data['username']).order_by('-id')
        for workout in workouts:
            workoutArray.append(workout)
        workoutSerializer = WorkoutSerializer(workoutArray, many=True)
        data = []
        return Response({'username': user.username, 'userrole': user.role, 'workouts': workoutSerializer.data, 'exercises': exerciseSerializer.data})


class GetSingleExercise(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        post = Exercise.objects.get(id=request.data['id'])
        pusername = ''
        prole = False
        musclegroups = []
        if (post.musclegroups):
            musclegroupObjects = post.musclegroups.all()
            for musclegroup in musclegroupObjects:
                musclegroups.append(musclegroup.name)
        if (post.user):
            pusername = post.user.username
        if (post.user):
            prole = post.user.role
        return Response({'title': post.title, 'musclegroups': musclegroups, 'image': post.image.url, 'content': post.content, 'date': post.date, 'user': pusername, 'userrole': prole, 'visibility': post.visibility, 'sets': post.sets, 'reps': post.reps})


class GetSingleWorkout(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        post = Workout.objects.get(id=request.data['id'])
        pusername = ''
        prole = False
        exercises = []
        musclegroups = []
        if (post.exercises):
            exerciseObjects = post.exercises.all()
            for exercise in exerciseObjects:
                exercises.append(exercise.title)
                if (exercise.musclegroups):
                    musclegroupObjects = exercise.musclegroups.all()
                    for musclegroup in musclegroupObjects:
                        musclegroups.append(musclegroup.name)
        if (post.user):
            pusername = post.user.username
        if (post.user):
            prole = post.user.role
        return Response({'title': post.title, 'exercises': exercises, 'musclegroups': list(set(musclegroups)), 'image': post.image.url, 'content': post.content, 'date': post.date, 'user': pusername, 'userrole': prole, 'visibility': post.visibility, 'duration': post.duration})


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def getFeedbackForPost(self):
        queryset = Post.objects.all()
        serializer_class = FeedbackSerializer


# class FeedViewSet(viewsets.ModelViewSet):
#     queryset = Exercise.objects.all()
#     serializer_class = ExerciseSerializer

#     def getPopularPublicExercises():
#         queryset = Exercise.objects.all()
#         serializer_class = ExerciseSerializer

#     def getPopularPublicWorkouts():
#         queryset = Workout.objects.all()
#         serializer_class = WorkoutSerializer
