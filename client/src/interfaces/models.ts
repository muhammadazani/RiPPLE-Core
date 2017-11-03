export interface Topic {
    id: number,
    name: string
};

export interface Question {
    id: number,
    difficulty: number,
    quality: number,

    topics: Topic[],

    content: string,
    explanation: string
    solution: Distractor,
    distractors: Distractor[],

    responses: QuestionResponse[]
};
export interface Distractor {
    id: number,
    content: string,
    isCorrect: boolean,
    response: string
}
export interface QuestionResponse {
    author: User,
    upVotes: number,
    solution: number,
    content: string
};

export interface Node {
    source: Topic,
    target: Topic,
    competency: number,
    attempts: number
};

export interface Course {
    courseCode: string,
    courseName: string,
    start: number,
    end: number,
    available: boolean
};

export interface User {
    id: number,
    name: string,
    bio: string,
    image: string,

    proficiencies?: string[],
    availableTime?: Date,
    connections: PeerConnection[]
};

export interface CourseUser {
    user: User,
    course: Course,
    roles: string[],

    error?: string
};

export interface PeerConnection {
    edgeStart: number, // ID of edge start. Corresponds to a User ID
    edgeEnd: number, // ID of edge end. Corresponds to a User ID
    type: "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner",
    topic: string,
    weight: number,
    date: Date, // Date the connection was made
    availableTime: Date
};

export interface UserSummary {
    name: string,
    image: string,
    reputation: number,
    questionsContributed: number,
    numberAnswers: number,
    numberComments: number
};

export interface Badge {
    id: number,
    name: string,
    category: "engagement" | "competencies" | "connections",
    description: string
};

export interface AcquiredBadge {
    id: number,
    badge: Badge,
    progress: number,
    dateAcquired: Date
};

export interface Notification {
    id: number,
    type: "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting",
    content: string,
    read: boolean
};

export interface Edge {
    source: Topic,
    target: Topic,
    competency: number,
    attempts: number
};

export interface QuestionBuilder {
    content: string,
    explanation: string,
    responses: {
        A: string,
        B: string,
        C: string,
        D: string
    },
    correctIndex: string,
    topics: Topic[]
};

export interface AuthorResponse {
    content: string,
    payloads: {
        [id: number]: string
    }
};

export interface QuestionUpload {
    question: AuthorResponse,
    explanation: AuthorResponse,
    responses: {
        A: AuthorResponse,
        B: AuthorResponse,
        C: AuthorResponse,
        D: AuthorResponse
    },
    topics: Topic[]
};