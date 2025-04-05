import AsyncStorage from '@react-native-async-storage/async-storage';

// ---------- Database ----------
export interface Flashcard {
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

// Add this function to your flashcardDB.ts file

export const getAllFlashcards = async (): Promise<Flashcard[]> => {
    try {
      // Get all keys in AsyncStorage
      const allKeys = await AsyncStorage.getAllKeys();
  
      // Filter keys to only include flashcard keys
      const flashcardKeys = allKeys.filter(key => key.startsWith(KEYS.FLASHCARD));
  
      // If no flashcards found, return empty array
      if (flashcardKeys.length === 0) {
        return [];
      }
  
      // Get all flashcards data
      const flashcardsData = await AsyncStorage.multiGet(flashcardKeys);
  
      // Parse JSON and convert to Flashcard objects
      const flashcards: Flashcard[] = flashcardsData
        .map(([_, value]) => (value ? JSON.parse(value) : null))
        .filter(item => item !== null);
  
      return flashcards;
    } catch (error) {
      handleError(error, 'getAllFlashcards');
      return [];
    }
  };

// ---------- Study Session funtions ----------
// ---------- Statistics funtions ----------
// ---------- User funtions ----------