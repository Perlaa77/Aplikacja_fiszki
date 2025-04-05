import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { getUser, updateUser, changeUserPassword, deleteUser } from '@/database/flashcardDB';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';

const ProfileScreen = () => {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        // W rzeczywistej aplikacji powinieneś mieć sposób na przechowywanie ID zalogowanego użytkownika
        const storedUserId = await AsyncStorage.getItem('currentUserId');
        if (storedUserId) {
          const id = parseInt(storedUserId);
          setUserId(id);
          const userData = await getUser(id);
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

    loadUser();
  }, []);

  const handleInputChange = (name: string, value: string) => {
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleUpdateProfile = async () => {
    if (!userId) return;

    try {
      await updateUser(userId, {
        username: formData.username,
        email: formData.email
      });
      Alert.alert('Success', 'Profile updated successfully');
      setEditing(false);
      // Refresh user data
      const updatedUser = await getUser(userId);
      if (updatedUser) setUser(updatedUser);
    } catch (error) {
      Alert.alert('Error', 'Failed to update profile');
      console.error(error);
    }
  };

  const handleChangePassword = async () => {
    if (!userId) return;

    if (formData.newPassword !== formData.confirmPassword) {
      Alert.alert('Error', 'New passwords do not match');
      return;
    }

    try {
      // W rzeczywistej aplikacji powinieneś zweryfikować currentPassword przed zmianą
      await changeUserPassword(userId, formData.newPassword);
      Alert.alert('Success', 'Password changed successfully');
      setFormData({
        ...formData,
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to change password');
      console.error(error);
    }
  };

  const handleDeleteAccount = async () => {
    if (!userId) return;

    Alert.alert(
      'Delete Account',
      'Are you sure you want to delete your account? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteUser(userId);
              await AsyncStorage.removeItem('currentUserId');
              Alert.alert('Success', 'Account deleted successfully');
              router.replace('/');
            } catch (error) {
              Alert.alert('Error', 'Failed to delete account');
              console.error(error);
            }
          }
        }
      ]
    );
  };

  const handleLogout = async () => {
    try {
      await AsyncStorage.removeItem('currentUserId');
      router.replace('/');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  if (!user) {
    return (
      <View style={styles.container}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Profile Settings</Text>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account Information</Text>
        
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Username</Text>
          {editing ? (
            <TextInput
              style={styles.input}
              value={formData.username}
              onChangeText={(text) => handleInputChange('username', text)}
            />
          ) : (
            <Text style={styles.value}>{user.username}</Text>
          )}
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Email</Text>
          {editing ? (
            <TextInput
              style={styles.input}
              value={formData.email}
              onChangeText={(text) => handleInputChange('email', text)}
              keyboardType="email-address"
            />
          ) : (
            <Text style={styles.value}>{user.email}</Text>
          )}
        </View>

        {editing ? (
          <View style={styles.buttonGroup}>
            <TouchableOpacity style={[styles.button, styles.saveButton]} onPress={handleUpdateProfile}>
              <Text style={styles.buttonText}>Save Changes</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.button, styles.cancelButton]} onPress={() => setEditing(false)}>
              <Text style={styles.buttonText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={[styles.button, styles.editButton]} onPress={() => setEditing(true)}>
            <Text style={styles.buttonText}>Edit Profile</Text>
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Change Password</Text>
        
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Current Password</Text>
          <TextInput
            style={styles.input}
            value={formData.currentPassword}
            onChangeText={(text) => handleInputChange('currentPassword', text)}
            secureTextEntry
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>New Password</Text>
          <TextInput
            style={styles.input}
            value={formData.newPassword}
            onChangeText={(text) => handleInputChange('newPassword', text)}
            secureTextEntry
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Confirm New Password</Text>
          <TextInput
            style={styles.input}
            value={formData.confirmPassword}
            onChangeText={(text) => handleInputChange('confirmPassword', text)}
            secureTextEntry
          />
        </View>

        <TouchableOpacity style={[styles.button, styles.changePasswordButton]} onPress={handleChangePassword}>
          <Text style={styles.buttonText}>Change Password</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <TouchableOpacity style={[styles.button, styles.logoutButton]} onPress={handleLogout}>
          <Text style={styles.buttonText}>Logout</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.deleteButton]} onPress={handleDeleteAccount}>
          <Text style={[styles.buttonText, styles.deleteButtonText]}>Delete Account</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  section: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 15,
    color: '#444',
  },
  inputGroup: {
    marginBottom: 15,
  },
  label: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    padding: 10,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  value: {
    fontSize: 16,
    padding: 10,
    color: '#333',
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  button: {
    padding: 12,
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
    fontWeight: '600',
    fontSize: 16,
  },
  editButton: {
    backgroundColor: '#4a90e2',
  },
  saveButton: {
    backgroundColor: '#2ecc71',
    flex: 1,
    marginRight: 5,
  },
  cancelButton: {
    backgroundColor: '#e74c3c',
    flex: 1,
    marginLeft: 5,
  },
  changePasswordButton: {
    backgroundColor: '#9b59b6',
  },
  logoutButton: {
    backgroundColor: '#3498db',
  },
  deleteButton: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#e74c3c',
    marginTop: 15,
  },
  deleteButtonText: {
    color: '#e74c3c',
  },
});

export default ProfileScreen;