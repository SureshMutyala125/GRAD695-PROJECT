from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Summary
from .summarizer_logic import generate_summary


def home(request):
    sm_avlble = Summary.objects.all()
    if request.user.is_authenticated and sm_avlble:
        summaries = Summary.objects.filter(user=request.user) 
    else:
        summaries = None
    print(summaries)
    return render(request, 'summarizer_app/home.html', {'summaries': summaries})


@login_required
def summarize_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        word_count = request.POST.get('word_count')
        youtube_url = request.POST.get('youtube_url')

        video_title, summary = generate_summary(youtube_url, word_count)

        summary_obj = Summary.objects.create(
            user=request.user,
            user_title=title,
            user_description=description,
            youtube_url=youtube_url,
            video_title=video_title,
            summary=summary
        )

        return redirect('summarize_result', summary_id=summary_obj.id)

    return render(request, 'summarizer_app/submit.html')


@login_required
def summarize_result(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id, user=request.user)
    return render(request, 'summarizer_app/result.html', {
        'user_title': summary.user_title,
        'user_description': summary.user_description,
        'video_title': summary.video_title,
        'summary': summary.summary
    })
