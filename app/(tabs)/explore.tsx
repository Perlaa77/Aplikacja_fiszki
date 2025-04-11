import { useState, useEffect } from 'react';
import { StyleSheet, Image, Platform, TouchableOpacity, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import { ScrollView } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { getAllFlashcards } from '../../database/flashcardDB';
import { getTopic } from '../../database/flashcardDB';
import { useColorScheme } from '@/hooks/useColorScheme';
import { useFocusEffect } from '@react-navigation/native';

export default function TabTwoScreen() {
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === 'dark';
  
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
          <ThemedText style={styles.emptyText}> Create some flashcards to start learning</ThemedText>
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
    <ScrollView 
      contentContainerStyle={[
        styles.scrollContainer,
        { backgroundColor: isDarkMode ? '#121212' : '#f5f7fa' }
      ]}
    >
      <ThemedView style={styles.headerContainer}>
        <ThemedText type="title" style={styles.headerTitle}>
          Learning
        </ThemedText>
        <ThemedText style={styles.headerSubtitle}>
          {flashcards.length > 0 
            ? `You have ${flashcards.length} cards to review` 
            : 'No flashcards available'}
        </ThemedText>
      </ThemedView>

      {renderFlashcard()}

      <ThemedView style={styles.navigationContainer}>
        <TouchableOpacity 
          onPress={handlePrevCard} 
          disabled={currentIndex === 0 || flashcards.length === 0}
          style={[
            styles.navButton,
            styles.navButtonPrev,
            (currentIndex === 0 || flashcards.length === 0) && styles.disabledButton
          ]}
        >
          <IconSymbol 
            size={20} 
            name="chevron.backward" 
            color={isDarkMode ? '#fff' : '#4a6da7'} 
          />
          <ThemedText style={styles.navButtonText}>Previous</ThemedText>
        </TouchableOpacity>
        
        <TouchableOpacity 
          onPress={handleNextCard} 
          disabled={currentIndex === flashcards.length - 1 || flashcards.length === 0}
          style={[
            styles.navButton,
            styles.navButtonNext,
            (currentIndex === flashcards.length - 1 || flashcards.length === 0) && styles.disabledButton
          ]}
        >
          <ThemedText style={styles.navButtonText}>Next</ThemedText>
          <IconSymbol 
            size={20} 
            name="chevron.forward" 
            color={isDarkMode ? '#fff' : '#4a6da7'} 
          />
        </TouchableOpacity>
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
    padding: 24,
    paddingBottom: 40,
  },
  headerContainer: {
    marginBottom: 24,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 8,
    color: '#FFB6C1',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  flashcardWrapper: {
    marginBottom: 32,
  },
  topicText: {
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 16,
    color: '#FFB6C1',
  },
  cardContainer: {
    marginHorizontal: 8,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 3,
  },
  card: {
    padding: 28,
    borderRadius: 16,
    minHeight: 240,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  cardCounter: {
    position: 'absolute',
    top: 16,
    right: 16,
    fontSize: 14,
    color: '#888',
    fontWeight: '500',
  },
  cardQuestion: {
    fontSize: 22,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
    lineHeight: 28,
  },
  cardAnswer: {
    fontSize: 22,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 20,
    color: '#4a6da7',
    lineHeight: 28,
  },
  cardHint: {
    fontStyle: 'italic',
    marginBottom: 16,
    color: '#666',
    textAlign: 'center',
  },
  cardInfo: {
    marginTop: 16,
    padding: 12,
    borderRadius: 8,
    backgroundColor: 'rgba(74, 109, 167, 0.1)',
    width: '100%',
    flexShrink: 1,
    overflow: 'visible',
    flexWrap: 'wrap',
    color: '#888',
    textAlign: 'center'
  },
  tapPrompt: {
    marginTop: 20,
    fontSize: 14,
    color: '#888',
    fontStyle: 'italic',
  },
  loadingContainer: {
    height: 240,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 20,
  },
  emptyContainer: {
    height: 240,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
    padding: 24,
    backgroundColor: '#fff',
    borderRadius: 16,
    marginHorizontal: 8,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
  },
  navigationContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 24,
  },
  navButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#FFB6C1',
  },
  navButtonPrev: {
    paddingRight: 16,
  },
  navButtonNext: {
    paddingLeft: 16,
  },
  navButtonText: {
    color: '#fff',
    fontWeight: '500',
    marginHorizontal: 8,
  },
  disabledButton: {
    opacity: 0.6,
  },
});