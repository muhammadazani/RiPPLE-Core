import { IRecommendation } from "../interfaces/models";
import RecommendationRepository from "../repositories/RecommendationRepository";

export default class RecommendationService {

    static findRecommendations(): Promise<IRecommendation[]> {
        return RecommendationRepository.findRecommendations();
    }

    static pendingRecommendations(): Promise<IRecommendation[]> {
        return RecommendationRepository.pendingRecommendations();
    }

    static reviewRecommendations(): Promise<IRecommendation[]> {
        return RecommendationRepository.reviewRecommendations();
    }
}
