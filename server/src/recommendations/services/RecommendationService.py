from ..models import PeerRecommendation, Recommendation

def get_user_find_recommendations(course_user):
    # Get the peer recommendations for the user
    peer_recommendations = PeerRecommendation.objects.filter(course_user=course_user)

    recommendations = []
    for peer_rec in peer_recommendations:

        # Get the recommendations with that peer recommendation
        recommendations = Recommendation.objects.filter(peer_recommendation=peer_rec, user_status="pending")

        if (len(recommendations) > 0):
            recommendation = {}

            recommendation['recommendedCourseUser'] = peer_rec.recommended_course_user.toJSON()
            recommendation['recommendedRole'] = []
            recommendation['dayTime'] = []
            for recommendation in recommendations:
                # Get the topic and study role of the reccommendedCourseUser
                recommended_role = {}
                user_request = recommendation.role_recommendation.user_request
                recommended_role['topic'] = user_request.topic.toJSON()
                recommended_role['studyRole'] = user_request.study_role.toJSON()
                recommendation['recommendedRole'].append(recommended_role)

                availability = recommendation.time_recommendation.recommended_user_availability
                dayTime = {
                        'day': availability.day.toJSON(),
                        'time': availability.time.toJSON()
                }

                recommendation['dayTime'].append(dayTime)

            recommendations.append(recommendation)
    return recommendations

def get_user_review_recommendations(course_user):
    # Get the peer recommendations for the user
    peer_recommendations = PeerRecommendation.objects.filter(recommended_course_user=course_user)

    recommendations = []
    for peer_rec in peer_recommendations:

        # Get the recommendations with that peer recommendation
        recommendations = recommendation.objects.filter(
            peer_recommendation=peer_rec,
            user_status="accepted",
            recommended_user_status="pending")

        if (len(recommendations) > 0):
            recommendation = {}

            recommendation['recommendedCourseUser'] = peer_rec.course_user.toJSON()
            recommendation['recommendedRole'] = []
            recommendation['dayTime'] = []
            for recommendation in recommendations:
                # Get the topic and study role of the reccommendedCourseUser
                recommended_role = {}
                recomended_user_request = recommendation.role_recommendation.recomended_user_request
                recommended_role['topic'] = recommended_role.topic.toJSON()
                recommended_role['studyRole'] = recomended_user_request.study_role.toJSON()
                recommendation['recommendedRole'].append(recommended_role)

                availability = recommendation.time_recommendation.user_availability
                dayTime = {
                        'day': availability.day.toJSON(),
                        'time': availability.time.toJSON()
                }

                recommendation['dayTime'].append(dayTime)

            recommendations.append(recommendation)

    return recommendations
