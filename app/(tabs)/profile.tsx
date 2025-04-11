import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert, ScrollView, ActivityIndicator } from 'react-native';
import { router, useRouter } from 'expo-router';
import { getUser, updateUser, changeUserPassword, deleteUser, clearUserSession, saveUserSession } from '@/database/flashcardDB';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useFocusEffect } from 'expo-router';
import React from 'react';


interface User {
  id: number;
  username: string;
  email: string;
  passwordHash: string;
}

export default function ProfileScreen() {
  const [user, setUser] = useState<User | null>(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const router = useRouter();

  const checkAuthAndLoadUser = React.useCallback(async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      console.log('Token from storage:', token);
      
      const userId = await AsyncStorage.getItem('currentUserId');
      console.log('UserID from storage:', userId);
      
      if (!token || !userId) {
        console.log('Missing auth data:', { token, userId });
        await clearUserSession();
        router.replace('/login');
        return null;
      }
      
      console.log('Fetching user with ID:', userId);
      const userData = await getUser(parseInt(userId));
      console.log('User data retrieved:', userData ? 'success' : 'failed');
      return userData;
    } catch (error) {
      console.error('Auth check error details:', error);
      await clearUserSession();
      router.replace('/login');
      return null;
    }
  }, [router]);

  useEffect(() => {
    let isMounted = true;
    
    const initialize = async () => {
      console.log('Initializing profile screen...');
      const userData = await checkAuthAndLoadUser();
      if (isMounted) {
        if (userData) {
          setUser(userData);
          setFormData({
            username: userData.username,
            email: userData.email,
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          });
        }
        setIsCheckingAuth(false);
      }
    };
    
    initialize();
    
    return () => {
      isMounted = false;
    };
  }, [checkAuthAndLoadUser]);

  useFocusEffect(
    React.useCallback(() => {
      console.log('Screen focused - refreshing data');
      if (!isCheckingAuth) {
        checkAuthAndLoadUser().then(userData => {
          if (userData) {
            setUser(userData);
          }
        });
      }
    }, [isCheckingAuth, checkAuthAndLoadUser])
  );

  // Handle profile update
  const handleUpdateProfile = async () => {
    if (!user) return;
    setIsLoading(true);
    
    try {
      await updateUser(user.id, {
        username: formData.username,
        email: formData.email
      });
      Alert.alert('Success', 'Profile updated successfully');
      setIsEditing(false);
      const updatedUser = await getUser(user.id);
      setUser(updatedUser);
    } catch (error) {
      Alert.alert('Error', 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleChangePassword = async () => {
    if (!user) return;
    
    if (!formData.currentPassword) {
      Alert.alert('Error', 'Please enter your current password');
      return;
    }
    
    if (formData.newPassword !== formData.confirmPassword) {
      Alert.alert('Error', "New passwords don't match");
      return;
    }
    
    if (formData.currentPassword === formData.newPassword) {
      Alert.alert('Error', "New password must be different from current password");
      return;
    }

    setIsLoading(true);

    try {
      if (user.passwordHash !== formData.currentPassword) {
        Alert.alert('Error', 'Current password is incorrect');
        setIsLoading(false);
        return;
      }
      
      await changeUserPassword(user.id, formData.newPassword);
      Alert.alert('Success', 'Password changed successfully');
      setFormData({
        ...formData,
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (error) {
      console.error('Error changing password:', error);
      Alert.alert('Error', 'Failed to change password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      setIsLoading(true);
      await Promise.all([
        AsyncStorage.removeItem('userToken'),
        AsyncStorage.removeItem('currentUserId')
      ]);
      router.replace('/login');
    } catch (error) {
      console.error('Logout error:', error);
      Alert.alert('Error', 'Failed to logout');
    } finally {
      setIsLoading(false);
    }
  };

  if (isCheckingAuth) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#888" />
      </View>
    );
  }

  if (!user) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#888" />
      </View>
    );
  }

  return (
    <ScrollView 
      contentContainerStyle={styles.scrollContainer}
      style={styles.container}
    >
      <ThemedText type="title" style={styles.title}>Profile</ThemedText>

      <ThemedView style={styles.section}>
        <ThemedText style={styles.sectionTitle}>Account Details</ThemedText>
        
        <View style={styles.inputGroup}>
          <ThemedText style={styles.label}>Username</ThemedText>
          {isEditing ? (
            <TextInput
              style={[styles.input, styles.lightText]}
              value={formData.username}
              onChangeText={(text) => setFormData({...formData, username: text})}
              placeholderTextColor="#aaa"
              autoCapitalize="none"
            />
          ) : (
            <ThemedText style={[styles.value, styles.lightText]}>{user.username}</ThemedText>
          )}
        </View>

        <View style={styles.inputGroup}>
          <ThemedText style={styles.label}>Email</ThemedText>
          {isEditing ? (
            <TextInput
              style={[styles.input, styles.lightText]}
              value={formData.email}
              onChangeText={(text) => setFormData({...formData, email: text})}
              keyboardType="email-address"
              placeholderTextColor="#aaa"
              autoCapitalize="none"
            />
          ) : (
            <ThemedText style={[styles.value, styles.lightText]}>{user.email}</ThemedText>
          )}
        </View>

        {isEditing ? (
          <View style={styles.buttonGroup}>
            <TouchableOpacity 
              style={[styles.button, styles.saveButton]} 
              onPress={handleUpdateProfile}
              disabled={isLoading}
            >
              {isLoading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <ThemedText style={styles.buttonText}>Save</ThemedText>
              )}
            </TouchableOpacity>
            <TouchableOpacity 
              style={[styles.button, styles.cancelButton]} 
              onPress={() => setIsEditing(false)}
              disabled={isLoading}
            >
              <ThemedText style={styles.buttonText}>Cancel</ThemedText>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity 
            style={[styles.button, styles.editButton]} 
            onPress={() => setIsEditing(true)}
          >
            <ThemedText style={styles.buttonText}>Edit</ThemedText>
          </TouchableOpacity>
        )}
      </ThemedView>

      <ThemedView style={styles.section}>
        <ThemedText style={styles.sectionTitle}>Change Password</ThemedText>
        
        <TextInput
          style={[styles.input, styles.lightText]}
          placeholder="Current Password"
          placeholderTextColor="#aaa"
          value={formData.currentPassword}
          onChangeText={(text) => setFormData({...formData, currentPassword: text})}
          secureTextEntry
          autoCapitalize="none"
        />
        
        <TextInput
          style={[styles.input, styles.lightText]}
          placeholder="New Password"
          placeholderTextColor="#aaa"
          value={formData.newPassword}
          onChangeText={(text) => setFormData({...formData, newPassword: text})}
          secureTextEntry
          autoCapitalize="none"
        />
        
        <TextInput
          style={[styles.input, styles.lightText]}
          placeholder="Confirm New Password"
          placeholderTextColor="#aaa"
          value={formData.confirmPassword}
          onChangeText={(text) => setFormData({...formData, confirmPassword: text})}
          secureTextEntry
          autoCapitalize="none"
        />
        
        <TouchableOpacity 
          style={[styles.button, styles.changePasswordButton]} 
          onPress={handleChangePassword}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <ThemedText style={styles.buttonText}>Change Password</ThemedText>
          )}
        </TouchableOpacity>
      </ThemedView>

      <View style={styles.footer}>
        <TouchableOpacity 
          style={[styles.button, styles.logoutButton]} 
          onPress={handleLogout}
        >
          <ThemedText style={styles.buttonText}>Logout</ThemedText>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  scrollContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#121212',
  },
  title: {
    textAlign: 'center',
    marginBottom: 20,
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFB6C1',
  },
  lightText: {
    color: '#fff',
  },
  section: {
    marginBottom: 20,
    padding: 20,
    borderRadius: 10,
    backgroundColor: '#1E1E1E',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 15,
    color: '#fff',
  },
  inputGroup: {
    marginBottom: 15,
  },
  label: {
    fontSize: 14,
    marginBottom: 5,
    color: '#aaa',
  },
  input: {
    height: 50,
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    backgroundColor: '#2A2A2A',
    color: '#fff',
  },
  value: {
    fontSize: 16,
    padding: 15,
    backgroundColor: '#2A2A2A',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#333',
    color: '#fff',
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  button: {
    borderRadius: 10,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 50,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
  },
  editButton: {
    backgroundColor: '#FFB6C1',
  },
  saveButton: {
    backgroundColor: '#FFCCE5',
    flex: 1,
  },
  cancelButton: {
    backgroundColor: '#FF8E8E',
    flex: 1,
  },
  changePasswordButton: {
    backgroundColor: '#FFB6C1',
  },
  logoutButton: {
    backgroundColor: '#FFB6C1',
  },
  footer: {
    marginTop: 20,
  },
});