<template>
  <div class="max-w-md mx-auto py-12">
    <div class="card space-y-8">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">Sign In</h2>
        <p class="mt-2 text-sm text-gray-600">Access your account to manage leaves</p>
      </div>

      <div v-if="authStore.error" class="p-4 bg-red-100 border border-red-200 text-red-700 rounded-md text-sm text-center">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="label">Email Address</label>
          <input
            v-model="email"
            type="email"
            required
            class="input-field"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="label mb-0">Password</label>
            <a href="#" class="text-xs text-blue-600 hover:text-blue-500 font-medium">Forgot password?</a>
          </div>
          <input
            v-model="password"
            type="password"
            required
            class="input-field"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="btn btn-primary w-full"
        >
          {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <div class="text-center">
        <p class="text-sm text-gray-600">
          Not a member?
          <router-link to="/register" class="text-blue-600 font-semibold hover:text-blue-500">
            Register now
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')

async function handleLogin() {
  try {
    await authStore.login(email.value, password.value)
    if (authStore.user?.role === 'employer') {
      router.push('/employer/dashboard')
    } else {
      router.push('/employee/dashboard')
    }
  } catch (error) {
    // Error is handled by authStore
  }
}
</script>
