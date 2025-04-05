import { useState, useEffect } from 'react';
import { StyleSheet, Image, Platform, TouchableOpacity, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { getAllFlashcards } from '../../database/flashcardDB';
import { getTopic } from '../../database/flashcardDB';

export default function TabTwoScreen() {
  const [flashcards, setFlashcards] = useState<Array<{
    id: number;
    topicId: number;
    front: string;
    frontHint?: string;
    back: string;
    backInfo?: string;
  }>>([]);
  
  const [currentTopic, setCurrentTopic] = useState<string>('No topic');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFlashcards = async () => {
      try {
        const cards = await getAllFlashcards();
        if (cards && Array.isArray(cards)) {
          setFlashcards(cards);
          // Pobierz temat dla pierwszej fiszki
          if (cards.length > 0) {
            const topic = await getTopic(cards[0].topicId);
            setCurrentTopic(topic?.name || 'No topic');
          }
        } else {
          setFlashcards([]);
        }
        setLoading(false);
      } catch (error) {
        console.error("Failed to load flashcards:", error);
        setFlashcards([]);
        setLoading(false);
      }
    };

    loadFlashcards();
  }, []);

  const handleNextCard = () => {
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowAnswer(false);
    }
  };

  const handlePrevCard = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setShowAnswer(false);
    }
  };

  const toggleAnswer = () => {
    setShowAnswer(!showAnswer);
  };

  const renderFlashcard = () => {
    if (loading) {
      return (
        <ThemedView style={styles.loadingContainer}>
          <ActivityIndicator size="large" />
          <ThemedText>Loading flashcards...</ThemedText>
        </ThemedView>
      );
    }

    if (flashcards.length === 0) {
      return (
        <ThemedView style={styles.emptyContainer}>
          <IconSymbol size={50} name="exclamationmark.triangle" color="#808080" />
          <ThemedText style={styles.emptyText}>No flashcards found</ThemedText>
          <ThemedText>Create some flashcards to start learning</ThemedText>
        </ThemedView>
      );
    }

    const currentCard = flashcards[currentIndex];
    
    return (
      <ThemedView style={styles.flashcardWrapper}>
        <ThemedText style={styles.topicText}>{currentTopic}</ThemedText>
        <TouchableOpacity activeOpacity={0.8} onPress={toggleAnswer} style={styles.cardContainer}>
          <ThemedView style={styles.card}>
            <ThemedText style={styles.cardCounter}>
              {currentIndex + 1} / {flashcards.length}
            </ThemedText>
            
            {!showAnswer ? (
              <>
                <ThemedText style={styles.cardQuestion}>{currentCard.front}</ThemedText>
                {currentCard.frontHint && (
                  <ThemedText style={styles.cardHint}>Hint: {currentCard.frontHint}</ThemedText>
                )}
                <ThemedText style={styles.tapPrompt}>Tap to see answer</ThemedText>
              </>
            ) : (
              <>
                <ThemedText style={styles.cardAnswer}>{currentCard.back}</ThemedText>
                {currentCard.backInfo && (
                  <ThemedText style={styles.cardInfo}>{currentCard.backInfo}</ThemedText>
                )}
                <ThemedText style={styles.tapPrompt}>Tap to see question</ThemedText>
              </>
            )}
          </ThemedView>
        </TouchableOpacity>
      </ThemedView>
    );
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }} headerImage={<></>}   >
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Learn from your flashcards!</ThemedText>
      </ThemedView>
      <ThemedText style={styles.instructions}>
        You can tap on your flashcard to see the answer.
      </ThemedText>

      {renderFlashcard()}

      <ThemedView style={styles.navigationButtonsContainer}>
        <TouchableOpacity 
          onPress={handlePrevCard} 
          disabled={currentIndex === 0 || flashcards.length === 0}
          style={[styles.navButton, (currentIndex === 0 || flashcards.length === 0) && styles.disabledButton]}
        >
          <IconSymbol size={24} name="chevron.backward" color={currentIndex === 0 || flashcards.length === 0 ? "#AAAAAA" : "#808080"} />
          <ThemedText style={[(currentIndex === 0 || flashcards.length === 0) && styles.disabledText]}>Previous</ThemedText>
        </TouchableOpacity>
        
        <TouchableOpacity 
          onPress={handleNextCard} 
          disabled={currentIndex === flashcards.length - 1 || flashcards.length === 0}
          style={[styles.navButton, (currentIndex === flashcards.length - 1 || flashcards.length === 0) && styles.disabledButton]}
        >
          <ThemedText style={[(currentIndex === flashcards.length - 1 || flashcards.length === 0) && styles.disabledText]}>Next</ThemedText>
          <IconSymbol size={24} name="chevron.forward" color={currentIndex === flashcards.length - 1 || flashcards.length === 0 ? "#AAAAAA" : "#808080"} />
        </TouchableOpacity>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  flashcardWrapper: {
    marginBottom: 20,
  },
  topicText: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#555',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 8,
  },
  instructions: {
    marginBottom: 24,
  },
  cardContainer: {
    marginHorizontal: 16,
    marginVertical: 8,
  },
  card: {
    padding: 20,
    borderRadius: 12,
    minHeight: 200,
    justifyContent: 'center',
    alignItems: 'center',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 2,
  },
  cardCounter: {
    position: 'absolute',
    top: 10,
    right: 10,
    fontSize: 12,
    opacity: 0.6,
  },
  cardQuestion: {
    fontSize: 20,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 16,
  },
  cardAnswer: {
    fontSize: 20,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 16,
  },
  cardHint: {
    fontStyle: 'italic',
    marginBottom: 12,
  },
  cardInfo: {
    marginTop: 8,
    padding: 10,
    borderRadius: 8,
    backgroundColor: 'rgba(128, 128, 128, 0.1)',
    width: '100%',
  },
  tapPrompt: {
    marginTop: 16,
    fontSize: 12,
    opacity: 0.6,
  },
  loadingContainer: {
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
  },
  emptyContainer: {
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    padding: 16,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    marginTop: 8,
  },
  navigationButtonsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 16,
    marginTop: 8,
  },
  navButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    gap: 4,
  },
  disabledButton: {
    opacity: 0.5,
  },
  disabledText: {
    opacity: 0.5,
  }
});