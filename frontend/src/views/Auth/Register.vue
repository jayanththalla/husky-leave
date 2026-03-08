<template>
  <div class="max-w-md mx-auto py-12">
    <div class="card space-y-8">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">Create Account</h2>
        <p class="mt-2 text-sm text-gray-600">Join the leave management system</p>
      </div>

      <div v-if="authStore.error" class="p-4 bg-red-100 border border-red-200 text-red-700 rounded-md text-sm text-center">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label class="label">Full Name</label>
          <input v-model="fullName" type="text" required class="input-field" placeholder="John Doe" />
        </div>

        <div>
          <label class="label">Email Address</label>
          <input v-model="email" type="email" required class="input-field" placeholder="you@example.com" />
        </div>

        <div>
          <label class="label">Your Role</label>
          <select v-model="role" required class="input-field">
            <option value="" disabled>Select your role</option>
            <option value="employee">Employee</option>
            <option value="employer">Employer</option>
          </select>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="label">Password</label>
            <input v-model="password" type="password" required class="input-field" placeholder="••••••••" />
          </div>
          <div>
            <label class="label">Confirm</label>
            <input v-model="confirmPassword" type="password" required class="input-field" placeholder="••••••••" />
          </div>
        </div>
        
        <div v-if="confirmPassword && password !== confirmPassword" class="text-xs text-red-600 font-medium">
          Passwords do not match
        </div>

        <button
          type="submit"
          :disabled="authStore.loading || (confirmPassword && password !== confirmPassword)"
          class="btn btn-primary w-full"
        >
          {{ authStore.loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <div class="text-center">
        <p class="text-sm text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-blue-600 font-semibold hover:text-blue-500">
            Sign In
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

const fullName = ref('')
const email = ref('')
const role = ref('')
const password = ref('')
const confirmPassword = ref('')

async function handleRegister() {
  if (password.value !== confirmPassword.value) return

  try {
    await authStore.register(email.value, fullName.value, role.value, password.value)
    if (role.value === 'employee') {
      router.push('/employee/dashboard')
    } else {
      router.push('/employer/dashboard')
    }
  } catch (error) {
    // Error is handled by authStore
  }
}
</script>
