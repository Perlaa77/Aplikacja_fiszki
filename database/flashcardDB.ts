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

  export interface Topic {
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

export const getAllTopics = async (): Promise<Topic[]> => {
  try {
    const allKeys = await AsyncStorage.getAllKeys();
    const topicKeys = allKeys.filter(key => key.startsWith(KEYS.TOPIC));
    if(topicKeys.length === 0) return [];

    const topicsData = await AsyncStorage.multiGet(topicKeys);
    
    const topics: Topic[] = topicsData
      .map(([_, value]) => (value ? JSON.parse(value) : null))
      .filter(item => item !== null);
    
      return topics;
  } catch (error) {
    handleError(error, 'getAllTopics');
    return [];
  }
}

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
// Save/Register user
export const saveUser = async (user: User): Promise<void> => {
  try {
      await AsyncStorage.setItem(
          `${KEYS.USER}${user.id}`,
          JSON.stringify(user)
      );
  } catch (error) {
      handleError(error, 'saveUser');
  }
};

// Get user by ID
export const getUser = async (id: number): Promise<User | null> => {
  try {
      const jsonValue = await AsyncStorage.getItem(`${KEYS.USER}${id}`);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
  } catch (error) {
      handleError(error, 'getUser');
      return null;
  }
};

// Get user by email (useful for login)
export const getUserByEmail = async (email: string): Promise<User | null> => {
  try {
      const allKeys = await AsyncStorage.getAllKeys();
      const userKeys = allKeys.filter(key => key.startsWith(KEYS.USER));
      
      for (const key of userKeys) {
          const userData = await AsyncStorage.getItem(key);
          if (userData) {
              const user = JSON.parse(userData);
              if (user.email === email) {
                  return user;
              }
          }
      }
      return null;
  } catch (error) {
      handleError(error, 'getUserByEmail');
      return null;
  }
};

// Update user (except password)
export const updateUser = async (id: number, updates: Partial<User>): Promise<void> => {
  try {
      const user = await getUser(id);
      if (!user) {
          throw new Error('User not found');
      }
      
      const updatedUser = { ...user, ...updates };
      await saveUser(updatedUser);
  } catch (error) {
      handleError(error, 'updateUser');
  }
};

// Change password
export const changeUserPassword = async (id: number, newPasswordHash: string): Promise<void> => {
  try {
      const user = await getUser(id);
      if (!user) {
          throw new Error('User not found');
      }
      
      const updatedUser = { ...user, passwordHash: newPasswordHash };
      await saveUser(updatedUser);
  } catch (error) {
      handleError(error, 'changeUserPassword');
  }
};

// Delete user
export const deleteUser = async (id: number): Promise<void> => {
  try {
      await AsyncStorage.removeItem(`${KEYS.USER}${id}`);
  } catch (error) {
      handleError(error, 'deleteUser');
  }
};

// Get all users (for admin purposes)
export const getAllUsers = async (): Promise<User[]> => {
  try {
      const allKeys = await AsyncStorage.getAllKeys();
      const userKeys = allKeys.filter(key => key.startsWith(KEYS.USER));
      
      if (userKeys.length === 0) {
          return [];
      }
      
      const usersData = await AsyncStorage.multiGet(userKeys);
      return usersData
          .map(([_, value]) => (value ? JSON.parse(value) : null))
          .filter(user => user !== null);
  } catch (error) {
      handleError(error, 'getAllUsers');
      return [];
  }
};

// Check if email is already registered
export const isEmailRegistered = async (email: string): Promise<boolean> => {
  try {
    const user = await getUserByEmail(email.toLowerCase());
    return user !== null;
  } catch (error) {
    console.error('Error checking email:', error);
    return false;
  }
};