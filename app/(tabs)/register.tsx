import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState } from 'react';
import { saveUser, isEmailRegistered } from '@/database/flashcardDB';
import { ThemedView } from '@/components/ThemedView';
import { ThemedText } from '@/components/ThemedText';
import { IconSymbol } from '@/components/ui/IconSymbol';

export default function RegisterScreen() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
  
    const handleRegister = async () => {
      if (!username || !email || !password || !confirmPassword) {
        alert('Please fill all fields');
        return;
      }
  
      if (password !== confirmPassword) {
        alert("Passwords don't match");
        return;
      }
  
      setIsLoading(true);
  
      try {
        if (await isEmailRegistered(email)) {
          alert('Email is already registered');
          return;
        }
  
        await saveUser({
          id: Date.now(),
          username,
          email,
          passwordHash: password
        });
  
        alert('Account created successfully');
        router.push('/login');
      } catch (error) {
        console.error(error);
        alert('Registration failed');
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <ScrollView contentContainerStyle={styles.container}>
        <ThemedText type="title" style={styles.title}>Register</ThemedText>
        
        <ThemedView style={styles.inputContainer}>
          <TextInput
            style={[styles.input, styles.darkText]}
            placeholder="Username"
            placeholderTextColor="#666"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />
          
          <TextInput
            style={[styles.input, styles.darkText]}
            placeholder="Email"
            placeholderTextColor="#666"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          
          <TextInput
            style={[styles.input, styles.darkText]}
            placeholder="Password"
            placeholderTextColor="#666"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            autoCapitalize="none"
          />
          
          <TextInput
            style={[styles.input, styles.darkText]}
            placeholder="Confirm Password"
            placeholderTextColor="#666"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
            secureTextEntry
            autoCapitalize="none"
          />
        </ThemedView>
  
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, isLoading && styles.disabledButton]}
          onPress={handleRegister}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <ThemedText style={[styles.buttonText]}>Register</ThemedText>
          )}
        </TouchableOpacity>
      </View>
  
        <TouchableOpacity onPress={() => router.push('/login')}>
          <ThemedText style={[styles.linkText, styles.darkText]}>Already have an account? Login</ThemedText>
        </TouchableOpacity>

        <TouchableOpacity 
                    style={styles.backButton}
                    onPress={() => router.replace('/(tabs)')}
                  >
                    <View style={styles.backButtonContent}>
                      <IconSymbol 
                        size={20} 
                        name="chevron.backward" 
                        color={'#FFB6C1'} 
                      />
                      <Text style={styles.backButtonText}>Back</Text>
                    </View>
                  </TouchableOpacity>
                  
      </ScrollView>
    );
}

const styles = StyleSheet.create({
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
      borderColor: '#ddd',
      borderRadius: 10,
      padding: 10,
      marginBottom: 15,
      backgroundColor: '#fff',
    },
    darkText: {
      color: '#C0C0C0',
    },
    buttonContainer: {
      alignItems: 'center',
      padding: 20,
    },
    button: {
      backgroundColor: '#007AFF',
      padding: 16,
      borderRadius: 10,
      width: '80%',
      alignItems: 'center',
      marginVertical: 10,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 3,
      elevation: 3,
    },
    buttonText: {
      color: 'white',
      fontSize: 18,
      fontWeight: '600',
    },
    disabledButton: {
      backgroundColor: '#FFD1DC', 
    },
    linkText: {
      textAlign: 'center',
      marginTop: 10,
    },
    backButton: {
      position: 'absolute',
      top: 40,
      left: 20,
      zIndex: 1,
    },
    backButtonContent: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    backButtonText: {
      color: '#FFB6C1',
      fontSize: 20,
      marginLeft: 5,
    },
});