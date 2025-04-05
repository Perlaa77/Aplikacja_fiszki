import AsyncStorage from '@react-native-async-storage/async-storage';

//Database
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

//Keys
const KEYS = {
    FLASHCARD: 'flashcard_',
    TOPIC: 'topic_',
    SESSION: 'session_',
    RESULT: 'result_',
    STATISTICS: 'statistics',
    USER: 'user_'  
}


//Operations on flashcards
