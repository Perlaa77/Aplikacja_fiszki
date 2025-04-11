import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
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
        Alert.alert('Error', 'Please enter both email and password');
        return;
      }
  
      setIsLoading(true);
      
      try {
        const user = await getUserByEmail(email);
        
        if (!user) {
          Alert.alert('Error', 'No account found with this email');
          setIsLoading(false);
          return;
        }
        
        // Simple password comparison (in production use bcrypt)
        if (user.passwordHash !== password) {
          Alert.alert('Error', 'Incorrect password');
          setIsLoading(false);
          return;
        }
        
        await AsyncStorage.multiSet([
          ['userToken', 'dummy-auth-token'],
          ['currentUserId', user.id.toString()]
        ]);
        
        // Confirm values were stored
        const storedUserId = await AsyncStorage.getItem('currentUserId');
        console.log('Stored user ID verification:', storedUserId);
        
        // Redirect to home screen after login
        router.replace('/(tabs)');
        
      } catch (error) {
        console.error('Login error:', error);
        Alert.alert('Error', 'Failed to login. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <ThemedView style={styles.mainContainer}>
        <ScrollView contentContainerStyle={styles.container}>
          <ThemedText type="title" style={styles.title}>Login</ThemedText>
          
          <ThemedView style={styles.inputContainer}>
            <TextInput
              style={[styles.input, styles.darkText]}
              placeholder="Email"
              placeholderTextColor="#888"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
            
            <TextInput
              style={[styles.input, styles.darkText]}
              placeholder="Password"
              placeholderTextColor="#888"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoCapitalize="none"
            />
          </ThemedView>
    
          <TouchableOpacity
            style={[styles.button, isLoading && styles.disabledButton]}
            onPress={handleLogin}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <ThemedText style={styles.buttonText}>Sign In</ThemedText>
            )}
          </TouchableOpacity>
    
          <TouchableOpacity onPress={() => router.push('/register')}>
            <ThemedText style={[styles.linkText, styles.darkText]}>Don't have an account? Register</ThemedText>
          </TouchableOpacity>
        </ScrollView>
      </ThemedView>
    );
}

const styles = StyleSheet.create({
    mainContainer: {
      flex: 1,
      backgroundColor: '#000',
    },
    container: {
      flexGrow: 1,
      justifyContent: 'center',
      padding: 20,
    },
    title: {
      textAlign: 'center',
      marginVertical: 20,
      fontSize: 24,
      fontWeight: 'bold',
      color: '#FFB6C1',
    },
    inputContainer: {
      marginVertical: 10,
    },
    input: {
      height: 50,
      borderWidth: 1,
      borderColor: '#333',
      borderRadius: 10,
      padding: 10,
      marginBottom: 15,
      backgroundColor: '#1a1a1a',
    },
    darkText: {
      color: '#FFF',
    },
    button: {
      borderRadius: 10,
      padding: 16,
      alignItems: 'center',
      marginVertical: 10,
      backgroundColor: '#FFB6C1',
    },
    disabledButton: {
      backgroundColor: '#FFD1DC',
    },
    buttonText: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#000',
    },
    linkText: {
      textAlign: 'center',
      marginTop: 10,
    },
});