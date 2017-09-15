import "whatwg-fetch";
import { API } from "./APIRepository";
import { Question, Topic } from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import f from "faker";

export default class QuestionRepository {
    static getMany(count: number): Promise<Question[]> {
        return fetch(`${API}/questions/all/`)
            .then(questions => questions.json())
            .then(questions => questions.map(x => {
                const question: Question = {
                    id: x.id,
                    difficulty: x.difficulty,
                    quality: x.quality,
                    solution: x.distractors.find(d => d.isCorrect === true),
                    distractors: x.distractors,
                    topics: x.topics.map(t => TopicRepository.topicPointer(t)),
                    content: x.content,
                    explanation: x.explanation,

                    responses: []
                };

                return question;
            }));
    }

    static search(sortField: string | undefined,
        sortOrder: string | undefined,
        filterField: string | undefined,
        query: string | undefined,
        page: string | undefined) {
        return fetch(`${API}/questions/search/`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sortField,
                sortOrder,
                filterField,
                query,
                page
            })
        })
            .then(questions => questions.json())
            .then(searchResult => ({
                totalItems: searchResult.totalItems,
                questions: searchResult.items.map(x => {
                    const question: Question = {
                        id: x.id,
                        difficulty: x.difficulty,
                        quality: x.quality,
                        solution: x.distractors.find(d => d.isCorrect === true),
                        distractors: x.distractors,
                        topics: x.topics.map(t => TopicRepository.topicPointer(t)),
                        content: x.content,
                        explanation: x.explanation,

                        responses: []
                    };

                    return question;
                }),
                page: searchResult.page
            }));
    }

    static submitResponse(distractorID: number) {
        return fetch(`${API}/questions/respond/`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                distractorID: distractorID
            })
        })
            .then(x => {
                return x.json()
                    .catch(_ => x);
            });
    }

    static submitRating(distractorID: number, rateType: string, rateValue: number) {
        return fetch(`${API}/questions/rate/`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                distractorID: distractorID,
                [`${rateType}`]: rateValue
            })
        })
            .then(x => {
                return x.json()
                    .catch(_ => x);
            });
    }

}
