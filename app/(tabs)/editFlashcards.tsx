// editFlashcard.tsx
import React, { useState, useEffect } from 'react';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, TouchableOpacity, Modal } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Flashcard, getAllTopics, getTopic, saveTopic, deleteTopic } from '../../database/flashcardDB';
import { Topic } from '../../database/flashcardDB';
import { saveFlashcard, getFlashcard, deleteFlashcard, getAllFlashcards } from '../../database/flashcardDB';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ScreenContainer } from 'react-native-screens';


export default function EditFlashcardScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const id = params.id as string;
  const topicId = params.topicId as string;

  const [flashcard, setFlashcard] = useState({
    id: parseInt(id || '0'),
    topicId: parseInt(topicId || '0'),
    front: '',
    frontHint: '',
    back: '',
    backInfo: ''
  });

  const [topic, setTopic] = useState({
    id: parseInt(id || '0'),
    name: '',
    description: ''
  });

  const [allFlashcards, setAllFlashcards] = useState<Flashcard[]>([]);
  const [allTopics, setAllTopics] = useState<Topic[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showTopicDropdown, setShowTopicDropdown] = useState(false);

  useEffect(() => {
    if (parseInt(id) === 0) {
      setFlashcard({
        id: 0,
        topicId: parseInt(topicId || '0'),
        front: '',
        frontHint: '',
        back: '',
        backInfo: ''
      });
    }
  }, [id, topicId]);

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        if (id && id !== '0') {
          const loadedFlashcard = await getFlashcard(parseInt(id));
          if (loadedFlashcard) {
            setFlashcard({
              id: loadedFlashcard.id,
              topicId: loadedFlashcard.topicId,
              front: loadedFlashcard.front,
              frontHint: loadedFlashcard.frontHint || '',
              back: loadedFlashcard.back,
              backInfo: loadedFlashcard.backInfo || ''
            });
          }
        }

        const flashcards = await getAllFlashcards();
        setAllFlashcards(flashcards);
        
        const topics = await getAllTopics();
        setAllTopics(topics);
        
        if (topicId && topicId !== '0') {
          const foundTopic = topics.find(t => t.id === parseInt(topicId));
          if (foundTopic) {
            setTopic({
              id: foundTopic.id,
              name: foundTopic.name,
              description: foundTopic.description || ''
            });
          }
        }
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [id, topicId]);

  const handleChange = (field: keyof typeof flashcard, value: string) => {
    setFlashcard(prev => ({ ...prev, [field]: value }));
  };

  const handleChangeTopic = (field: keyof typeof topic, value: string) => {
    setTopic(prev => ({ ...prev, [field]: value }));
  };

  const handleTopic = async () => {
    if (!topic.name.trim()) {
      setError('Topic title is required');
      return;
    }
    setIsLoading(true);

    try {
      const topicToSave = { ...topic };

      if (topicToSave.id === 0) {
        topicToSave.id = Date.now();
      }

      await saveTopic(topicToSave);
      
      if (topic.id === 0) {
        setTopic({
          id: topicToSave.id,
          name: '',
          description: ''
        });
      }

      const updatedTopics = await getAllTopics();
      setAllTopics(updatedTopics);
    } catch (err) {
      setError('Failed to save topic');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!flashcard.front.trim() || !flashcard.back.trim()) {
      setError('Front and back content are required');
      return;
    }

    setIsLoading(true);
    try {
      const flashcardToSave = { ...flashcard };

      if (flashcardToSave.id === 0) {
        flashcardToSave.id = Date.now();
      }

      await saveFlashcard(flashcardToSave);
      
      if (flashcard.id === 0) {
        setFlashcard(prev => ({
          ...prev,
          id: 0,
          front: '',
          frontHint: '',
          back: '',
          backInfo: ''
        }));
      }

      const updatedFlashcards = await getAllFlashcards();
      setAllFlashcards(updatedFlashcards);
    } catch (err) {
      setError('Failed to save flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (cardId: number) => {
    setIsLoading(true);
    try {
      await deleteFlashcard(cardId);
      const updatedFlashcards = await getAllFlashcards();
      setAllFlashcards(updatedFlashcards);
      if (cardId === flashcard.id) {
        router.back();
      }
    } catch (err) {
      setError('Failed to delete flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectTopic = (selectedTopic: Topic) => {
    setFlashcard(prev => ({ ...prev, topicId: selectedTopic.id }));
    setShowTopicDropdown(false);
  };

  const getSelectedTopicName = () => {
    if (flashcard.topicId === 0) return 'Select a Topic';
    const selectedTopic = allTopics.find(t => t.id === flashcard.topicId);
    return selectedTopic ? selectedTopic.name : 'Select a Topic';
  };

  if (isLoading) return <ThemedView style={styles.container}><ThemedText>Loading...</ThemedText></ThemedView>;

  return (
    <ParallaxScrollView 
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }} headerImage={<></>}   >
      {error && <ThemedText style={styles.error}>{error}</ThemedText>}

    {/* TOPICS */}
    
      <ThemedText style={styles.label}>Topic Title</ThemedText>
      <TextInput
        style={styles.input}
        value={topic.name}
        onChangeText={(text) => handleChangeTopic('name', text)}
        placeholder="Enter title"
        multiline
      />

      <ThemedText style={styles.label}>Topic Description</ThemedText>
      <TextInput
        style={styles.input}
        value={topic.description}
        onChangeText={(text) => handleChangeTopic('description', text)}
        placeholder="Enter description (optional)"
        multiline
      />

      <View style={styles.buttonContainer}>
        <Button title="Save Topic" onPress={handleTopic} disabled={isLoading} />
      </View>

    {/* FLASHCARDS */}

      {/* Topic Dropdown */}
      <ThemedText style={styles.label}>Select Topic for Flashcard</ThemedText>
      <TouchableOpacity 
        style={styles.dropdown}
        onPress={() => setShowTopicDropdown(true)}
      >
        <ThemedText>{getSelectedTopicName()}</ThemedText>
      </TouchableOpacity>

      {/* Topic Selection Modal */}
      <Modal
        visible={showTopicDropdown}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setShowTopicDropdown(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <ThemedText style={styles.modalTitle}>Select a Topic</ThemedText>
            
            <ScrollView style={styles.topicList}>
              {allTopics.length === 0 ? (
                <ThemedText style={styles.noTopicsText}>No topics available. Create one first.</ThemedText>
              ) : (
                allTopics.map((t) => (
                  <TouchableOpacity
                    key={t.id}
                    style={[
                      styles.topicItem,
                      t.id === flashcard.topicId && styles.selectedTopicItem
                    ]}
                    onPress={() => handleSelectTopic(t)}
                  >
                    <ThemedText style={styles.topicItemText}>{t.name}</ThemedText>
                  </TouchableOpacity>
                ))
              )}
            </ScrollView>
            
            <Button title="Cancel" onPress={() => setShowTopicDropdown(false)} />
          </View>
        </View>
      </Modal>

      <ThemedText style={styles.label}>Front (Question)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.front}
        onChangeText={(text) => handleChange('front', text)}
        placeholder="Enter question"
        multiline
      />
      
      <ThemedText style={styles.label}>Front Hint (Optional)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.frontHint || ''}
        onChangeText={(text) => handleChange('frontHint', text)}
        placeholder="Enter hint"
        multiline
      />
      
      <ThemedText style={styles.label}>Back (Answer)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.back}
        onChangeText={(text) => handleChange('back', text)}
        placeholder="Enter answer"
        multiline
      />
      
      <ThemedText style={styles.label}>Additional Info (Optional)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.backInfo || ''}
        onChangeText={(text) => handleChange('backInfo', text)}
        placeholder="Enter additional information"
        multiline
      />
      
      <View style={styles.buttonContainer}>
        <Button 
          title="Save" 
          onPress={handleSave} 
          disabled={isLoading || flashcard.topicId === 0} 
        />
      </View>

      <ThemedText style={styles.sectionTitle}>All Flashcards (tap to delete)</ThemedText>
      <View style={styles.flashcardsContainer}>
        {allFlashcards.length === 0 ? (
          <ThemedText style={styles.noCardsText}>No flashcards found</ThemedText>
        ) : (
          allFlashcards.map((card) => (
            <TouchableOpacity 
              key={card.id} 
              style={styles.cardContainer}
              onPress={() => handleDelete(card.id)}
            >
              <ThemedText style={styles.cardText} numberOfLines={1}>Topic: {card.topicId}</ThemedText>
              <ThemedText style={styles.cardText} numberOfLines={2}>Front: {card.front}</ThemedText>
              <ThemedText style={styles.cardText} numberOfLines={1}>Hint: {card.frontHint}</ThemedText>
              <ThemedText style={styles.cardText} numberOfLines={2}>Back: {card.back}</ThemedText>
              <ThemedText style={styles.cardText} numberOfLines={1}>Back Info: {card.backInfo}</ThemedText>
            </TouchableOpacity>
          ))
        )}
      </View>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 12,
    marginBottom: 4,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    padding: 10,
    fontSize: 16,
    minHeight: 80,
    marginBottom: 12,
    color: '#f8f8f8',
  },
  dropdown: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    padding: 14,
    marginBottom: 20,
    backgroundColor: '#f5f5f5',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 24,
  },
  error: {
    color: 'red',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 24,
    marginBottom: 12,
  },
  flashcardsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 8,
  },
  cardContainer: {
    width: '48%',
    marginBottom: 12,
    justifyContent: 'space-between',
    backgroundColor: '#f8f8f8',
    borderRadius: 8,
    padding: 12,
  },
  cardContent: {
    flex: 1,
    marginRight: 12,
  },
  cardText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 4,
  },
  deleteButton: {
    backgroundColor: '#ff4444',
    borderRadius: 4,
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  deleteButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  noCardsText: {
    color: '#666',
    textAlign: 'center',
    marginVertical: 16,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    width: '80%',
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 20,
    maxHeight: '70%',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center',
  },
  topicList: {
    marginBottom: 16,
    maxHeight: 300,
  },
  topicItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  selectedTopicItem: {
    backgroundColor: '#e6f7ff',
  },
  topicItemText: {
    fontSize: 16,
  },
  noTopicsText: {
    textAlign: 'center',
    marginVertical: 20,
    color: '#666',
  },
});