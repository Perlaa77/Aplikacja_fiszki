import AsyncStorage from '@react-native-async-storage/async-storage';

// ---------- Database ----------
interface Flashcard {
    id: number;
    topicId: number;
    front: string;
    frontHint?: string;
    back: string;
    backInfo?: string;
  }

  interface Topic {
    id: number;
    name: string;
    description?: string;
  }

  interface StudySession {
    id: number;
    flashcardIds: number[];
    topicIds: number[];
    mode: 'classic' | 'test';
    timeTracking: boolean;
    startTime: Date;
    endTime: Date;
    duration: number; //Date?
    flashcardsSeen: number;
    correctAnswers: number;
    results?: FlashcardResult[];
  }

  interface FlashcardResult {
    flashcardId: number;
    isCorrect: boolean;
    userAnswer?: string;
    startTime: Date;
    endTime: Date;
    duration: number; //Date?
  }

  interface Statistics {
    totalSessions: number;
    totalFlashcardsSeen: number;
    totalCorrectAnswers: number;
    totalIncorrectAnswers: number;
    totalTimeSpent: number;
    lastStudyDate: number;
    topicStats: {
      [topic: string]: {
        flashcardsSeen: number;
        correctAnswers: number;
        incorrectAnswers: number;
        averageTime: number;
      }
    };
  }

  interface User {
    id: number;
    username: string;
    email: string;
    passwordHash: string;
  }

// ---------- Keys ----------
const KEYS = {
    FLASHCARD: 'flashcard_',
    TOPIC: 'topic_',
    SESSION: 'session_',
    RESULT: 'result_',
    STATISTICS: 'statistics',
    USER: 'user_'  
}

// ---------- Handle errors ----------
const handleError = (error: any, operation: string) => {
    console.error(`Error during ${operation}:`, error);
    throw error;
};

// ---------- Flashcard funtions ----------
//Save
export const saveFlashcard = async (flashcard: Flashcard): Promise<void> => {
    try {
        await AsyncStorage.setItem(
            `${KEYS.FLASHCARD}${flashcard.id}`,
            JSON.stringify(flashcard)
        );
    } catch (error) {
        handleError(error, 'saveFlashcard');
    }
};

//Get
export const getFlashcard = async (id: number): Promise<Flashcard | null> => {
    try {
        const jsonValue = await AsyncStorage.getItem(`${KEYS.FLASHCARD}${id}`);
        return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (error) {
        handleError(error, 'getFlashcard');
        return null;
    }
};

//Delete
export const deleteFlashcard = async (id: number): Promise<void> => {
    try {
        await AsyncStorage.removeItem(`${KEYS.FLASHCARD}${id}`);
    } catch (error) {
        handleError(error, 'deleteFlashcard');
    }
};

// ---------- Topic funtions ----------
//Save
export const saveTopic = async (topic: Topic): Promise<void> => {
    try {
        await AsyncStorage.setItem(
            `${KEYS.TOPIC}${topic.id}`,
            JSON.stringify(topic)
        );
    } catch (error) {
        handleError(error, 'saveTopic');
    }
};

//Get
export const getTopic = async (id: number): Promise<Topic | null> => {
    try {
        const jsonValue = await AsyncStorage.getItem(`${KEYS.TOPIC}${id}`);
        return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (error) {
        handleError(error, 'getTopic');
        return null;
    }
};

//Delete
export const deleteTopic = async (id: number): Promise<void> => {
    try {
        await AsyncStorage.removeItem(`${KEYS.TOPIC}${id}`);
    } catch (error) {
        handleError(error, 'deleteTopic');
    }
};

// ---------- Study Session funtions ----------
// ---------- Statistics funtions ----------
// ---------- User funtions ----------