import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isEmployee = computed(() => user.value?.role === 'employee')
  const isEmployer = computed(() => user.value?.role === 'employer')

  function initializeFromStorage() {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  async function register(email, fullName, role, password) {
    loading.value = true
    error.value = null
    try {
      const response = await client.post('/api/users/register', {
        email,
        full_name: fullName,
        role,
        password,
      })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const response = await client.post('/api/users/login', {
        email,
        password,
      })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isEmployee,
    isEmployer,
    register,
    login,
    logout,
    initializeFromStorage,
  }
})
