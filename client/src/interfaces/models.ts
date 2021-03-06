export interface ITopic {
    id: number,
    name: string
};
export interface IEngagementType extends ITopic {
};

export interface IEdge {
    source: ITopic,
    target: ITopic,
    competency: number,
    attempts: number
};
export interface ICompareSet {
    topics: ITopic[], // Node List
    ownScores: IEdge[], // IEdge list of self
    compareAgainst: IEdge[] // IEdge list of other
};

export interface IQuestion {
    id: number,
    difficulty: number,
    quality: number,

    topics: ITopic[],

    content: string,
    explanation: string
    solution: IDistractor,
    distractors: IDistractor[],
    responseCount: number,
    canEdit?: boolean,
    createdAt?: number
};

export interface IDistractor {
    id: number,
    content: string,
    isCorrect: boolean,
    response: string
}
export interface IQuestionResponse {
    author: IUser,
    upVotes: number,
    solution: number,
    content: string
};

export interface IReportQuestion {
    question: number,
    reason: string[]
};

export interface IServerReportAggregate {
    questionID: number,
    totalReports: number,
    lastReport: number
}

export interface IServerReport {
    author: string,
    createdAt: number,
    reasons: IServerReason[]
}

export interface IServerReason {
    reasonText: string,
    reportReason: string
}

export interface IServerReportFull {
    reports: (IServerReportAggregate | IServerReport)[][]
    [key: number]: (IServerReportAggregate | IServerReport)[]
}

export interface IReportAggregate {
    questionID: number,
    totalReports: number,
    lastReport: string
}

export interface IReport {
    createdAt: string,
    author: string,
    reason: string
}

export interface IReasonList {
    reasonList: string[]
}

export interface INetworkResponse {
    error?: string
}

export interface IUser {
    id: number,
    name: string,
    bio: string,
    image: string,

    proficiencies?: string[],
    availableTime?: Date,
    connections: IPeerConnection[]
};

export interface ICourse {
    courseID: string,
    courseCode: string,
    courseName: string,
    courseSem: string,
    start?: number,
    end?: number,
    available?: boolean
};

export interface ICourseUser {
    user: IUser,
    course: ICourse,
    roles: string[],
};

export interface IConsentForm {
    content: string,
    author: ICourseUser,

    error?: string
};

export interface IConsentUpload {
    payload?: IAuthorResponse | undefined,
    author: ICourseUser
};

export interface IPeerConnection {
    edgeStart: number, // ID of edge start. Corresponds to a User ID
    edgeEnd: number, // ID of edge end. Corresponds to a User ID
    type: "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner",
    topic: string,
    weight: number,
    date: Date, // Date the connection was made
    availableTime: Date
};

export interface IUserSummary {
    id?: number
    firstName?: string,
    lastName?: string,
    image?: string,

    rank: number,
    questionsAuthored: number,
    questionsAnswered: number,
    questionsAnsweredCorrectly: number,
    questionsRated: number,
    achievementsEarned: number
};

export interface IBadge {
    key: string,
    name: string,
    description: string,
    category: "engagement" | "competencies" | "connections",
    count: number,
    progress: number,
    icon: string,
    dateAcquired: Date
};

export interface INotification {
    id: number,
    name: string,
    description: string,
    icon: string,
    created?: number
};

export interface ISnackbarNotification{
    name: string,
    description: string,
    icon: string
}

export interface IQuestionBuilder {
    content: string,
    explanation: string,
    responses: {
        A: string,
        B: string,
        C: string,
        D: string
    },
    correctIndex: string,
    topics: ITopic[],
    createdAt?: string
};

export interface IAuthorResponse {
    content: string,
    isCorrect: boolean,
    payloads: {
        [id: number]: string
    }
};

export interface IQuestionUpload {
    question?: IAuthorResponse,
    explanation?: IAuthorResponse,
    responses: {
        A?: IAuthorResponse,
        B?: IAuthorResponse,
        C?: IAuthorResponse,
        D?: IAuthorResponse
    },
    topics?: ITopic[]
};

export interface IDay {
    id: number,
    day: string
}

export interface ITime {
    id: number,
    start: {
        time: string,
        hour: number
    },
    end: {
        time: string,
        hour: number
    }
}

export interface IAvailability {
    id: number,
    courseUser: ICourseUser,
    day: IDay,
    time: ITime
}

export interface ICourseAvailability {
    courseUser: ICourseUser,
    day: number,
    time: number,
    entries: number
};

export interface IDayTime {
    day: number,
    time: number
};

export interface ILink {
    text: string,
    href: string
    icon?: string
    submenu?: ILink[]
};

export interface IServerResponse<T> {
    error: string,
    notifications: INotification[]
    data: T
}

export interface StudyRole {
    id: number,
    role: string,
    description: string
}

export interface IAvailableRole {
    courseUser: ICourseUser,
    topic: ITopic,
    studyRole: IStudyRole
}

export interface IStudyRole {
    id: number,
    role: string,
    description: string
}

export interface IAvailableRole {
    courseUser: ICourseUser,
    topic: ITopic,
    studyRole: IStudyRole
}

export interface ISearch {
    sortField: string,
    sortDesc: boolean,
    filterField: string,
    query: string,
    page: number,
    filterTopics: number[]
};
