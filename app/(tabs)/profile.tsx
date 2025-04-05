import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert, ScrollView, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { getUser, updateUser, changeUserPassword, deleteUser } from '@/database/flashcardDB';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function ProfileScreen() {
    const [user, setUser] = useState<any>(null);
    const [formData, setFormData] = useState({
      username: '',
      email: '',
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    const [isEditing, setIsEditing] = useState(false);
    const router = useRouter();
  
    useEffect(() => {
      const loadUserData = async () => {
        try {
          const userId = await AsyncStorage.getItem('userId');
          if (userId) {
            const userData = await getUser(parseInt(userId));
            if (userData) {
              setUser(userData);
              setFormData({
                ...formData,
                username: userData.username,
                email: userData.email
              });
            }
          }
        } catch (error) {
          console.error('Error loading user:', error);
        }
      };
  
      loadUserData();
    }, []);
  
    const handleUpdateProfile = async () => {
      if (!user) return;
  
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
      }
    };
  
    const handleChangePassword = async () => {
      if (formData.newPassword !== formData.confirmPassword) {
        Alert.alert('Error', "Passwords don't match");
        return;
      }
  
      try {
        await changeUserPassword(user.id, formData.newPassword);
        Alert.alert('Success', 'Password changed successfully');
        setFormData({...formData, newPassword: '', confirmPassword: ''});
      } catch (error) {
        Alert.alert('Error', 'Failed to change password');
      }
    };
  
    const handleLogout = async () => {
      await AsyncStorage.removeItem('userToken');
      await AsyncStorage.removeItem('userId');
      router.replace('/');
    };
  
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
              <TouchableOpacity style={[styles.button, styles.saveButton]} onPress={handleUpdateProfile}>
                <ThemedText style={styles.buttonText}>Save</ThemedText>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.button, styles.cancelButton]} onPress={() => setIsEditing(false)}>
                <ThemedText style={styles.buttonText}>Cancel</ThemedText>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={[styles.button, styles.editButton]} onPress={() => setIsEditing(true)}>
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
          
          <TouchableOpacity style={[styles.button, styles.changePasswordButton]} onPress={handleChangePassword}>
            <ThemedText style={styles.buttonText}>Change Password</ThemedText>
          </TouchableOpacity>
        </ThemedView>
  
        <View style={styles.footer}>
          <TouchableOpacity style={[styles.button, styles.logoutButton]} onPress={handleLogout}>
            <ThemedText style={styles.buttonText}>Logout</ThemedText>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#121212', // Ciemne tło
    },
    scrollContainer: {
      padding: 20,
      paddingBottom: 40,
    },
    loadingContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#121212', // Ciemne tło
    },
    title: {
      textAlign: 'center',
      marginBottom: 20,
      fontSize: 24,
      fontWeight: 'bold',
      color: '#FFB6C1', // Biały tekst
    },
    lightText: {
      color: '#fff', // Biały tekst dla zawartości
    },
    section: {
      marginBottom: 20,
      padding: 20,
      borderRadius: 10,
      backgroundColor: '#1E1E1E', // Ciemniejszy odcień dla sekcji
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
      color: '#fff', // Biały tekst
    },
    inputGroup: {
      marginBottom: 15,
    },
    label: {
      fontSize: 14,
      marginBottom: 5,
      color: '#aaa', // Jasnoszary tekst dla etykiet
    },
    input: {
      height: 50,
      borderWidth: 1,
      borderColor: '#333', // Ciemniejsza ramka
      borderRadius: 10,
      padding: 15,
      marginBottom: 15,
      backgroundColor: '#2A2A2A', // Ciemne tło dla inputów
      color: '#fff', // Biały tekst w inputach
    },
    value: {
      fontSize: 16,
      padding: 15,
      backgroundColor: '#2A2A2A', // Ciemne tło dla wartości
      borderRadius: 10,
      borderWidth: 1,
      borderColor: '#333', // Ciemniejsza ramka
      color: '#fff', // Biały tekst
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
      backgroundColor: '#FFB6C1', // Jasny róż/czerwony
    },
    saveButton: {
      backgroundColor: '#FFCCE5', // Jasny róż/czerwony
      flex: 1,
    },
    cancelButton: {
      backgroundColor: '#FF8E8E', // Jaśniejszy róż/czerwony dla cancel
      flex: 1,
    },
    changePasswordButton: {
      backgroundColor: '#FFB6C1', // Jasny róż/czerwony
    },
    logoutButton: {
      backgroundColor: '#FFB6C1', // Jasny róż/czerwony
    },
    footer: {
      marginTop: 20,
    },
});