import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useEffect, useState } from 'react';
import { getUserByEmail } from '@/database/flashcardDB';


export default function LoginScreen() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
  
    const handleLogin = async () => {
      if (!email || !password) {
        Alert.alert('Błąd', 'Wprowadź email i hasło');
        return;
      }
  
      setIsLoading(true);
  
      try {
        // 1. Znajdź użytkownika po emailu
        const user = await getUserByEmail(email);
        
        // 2. Sprawdź czy użytkownik istnieje i hasło jest poprawne (wersja bez hashowania)
        if (!user || password !== user.passwordHash) {
          Alert.alert('Błąd', 'Nieprawidłowy email lub hasło');
          setIsLoading(false);
          return;
        }
        
        // 3. Zapisz ID użytkownika jako prostą sesję
        await AsyncStorage.setItem('currentUserId', user.id.toString());
        
        // 4. Przekieruj do głównego ekranu
        router.replace('/');
        
      } catch (error) {
        console.error('Błąd logowania:', error);
        Alert.alert('Błąd', 'Wystąpił problem podczas logowania');
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Logowanie</Text>
        
        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />
        
        <TextInput
          style={styles.input}
          placeholder="Hasło"
          placeholderTextColor="#888"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TouchableOpacity 
          style={styles.button} 
          onPress={handleLogin}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Zaloguj się</Text>
          )}
        </TouchableOpacity>
        
        <View style={styles.footer}>
          <Text style={styles.footerText}>Nie masz konta?</Text>
          <TouchableOpacity onPress={() => router.push('/register')}>
            <Text style={styles.footerLink}>Zarejestruj się</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      padding: 20,
      backgroundColor: '#fff',
    },
    title: {
      fontSize: 28,
      fontWeight: 'bold',
      marginBottom: 30,
      textAlign: 'center',
      color: '#333',
    },
    input: {
      height: 50,
      borderColor: '#ddd',
      borderWidth: 1,
      borderRadius: 8,
      paddingHorizontal: 15,
      marginBottom: 15,
      backgroundColor: '#f9f9f9',
    },
    button: {
      backgroundColor: '#007AFF',
      padding: 15,
      borderRadius: 8,
      alignItems: 'center',
      marginTop: 10,
    },
    buttonText: {
      color: '#fff',
      fontWeight: 'bold',
      fontSize: 16,
    },
    footer: {
      flexDirection: 'row',
      justifyContent: 'center',
      marginTop: 20,
    },
    footerText: {
      color: '#666',
      marginRight: 5,
    },
    footerLink: {
      color: '#007AFF',
      fontWeight: 'bold',
    },
  });