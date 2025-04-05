import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState } from 'react';
import { saveUser, isEmailRegistered } from '@/database/flashcardDB';

export default function RegisterScreen() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
  
    const handleRegister = async () => {
      if (!username || !email || !password || !confirmPassword) {
        Alert.alert('Błąd', 'Wypełnij wszystkie pola');
        return;
      }
  
      if (password !== confirmPassword) {
        Alert.alert('Błąd', 'Hasła nie są identyczne');
        return;
      }
  
      // Walidacja emaila
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        Alert.alert('Błąd', 'Wprowadź poprawny adres email');
        return;
      }
  
      setIsLoading(true);
  
      try {
        // Sprawdź czy email jest już zarejestrowany
        const emailRegistered = await isEmailRegistered(email);
        if (emailRegistered) {
          Alert.alert('Błąd', 'Ten email jest już zarejestrowany');
          setIsLoading(false);
          return;
        }
  
        // Utwórz nowego użytkownika (w rzeczywistej aplikacji powinno się zahashować hasło!)
        const newUser = {
          id: Date.now(), // Używamy timestamp jako ID
          username,
          email: email.toLowerCase(), // Zawsze zapisuj email małymi literami
          passwordHash: password // UWAGA: W prawdziwej aplikacji musisz zahashować hasło!
        };
  
        // Zapisz użytkownika
        await saveUser(newUser);
  
        Alert.alert('Sukces', 'Konto zostało utworzone pomyślnie');
        router.push('/login');
      } catch (error) {
        console.error('Błąd rejestracji:', error);
        Alert.alert('Błąd', `Wystąpił problem podczas rejestracji: ${error || 'Spróbuj ponownie'}`);
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Rejestracja</Text>
        
        <TextInput
          style={styles.input}
          placeholder="Nazwa użytkownika"
          placeholderTextColor="#888"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="words"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Email (np. twojemail@example.com)"
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Hasło (min. 6 znaków)"
          placeholderTextColor="#888"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TextInput
          style={styles.input}
          placeholder="Potwierdź hasło"
          placeholderTextColor="#888"
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry
        />
        
        <TouchableOpacity 
          style={styles.button} 
          onPress={handleRegister}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Zarejestruj się</Text>
          )}
        </TouchableOpacity>
        
        <View style={styles.footer}>
          <Text style={styles.footerText}>Masz już konto?</Text>
          <TouchableOpacity onPress={() => router.push('/login')}>
            <Text style={styles.footerLink}>Zaloguj się</Text>
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
      backgroundColor: '#34C759',
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
      color: '#404040',
      marginRight: 5,
    },
    footerLink: {
      color: '#007AFF',
      fontWeight: 'bold',
    },
  });