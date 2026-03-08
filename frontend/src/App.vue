<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navigation -->
    <nav class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <span class="text-xl font-bold text-blue-600 tracking-tight">LeaveManager</span>
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <template v-if="authStore.isLoggedIn">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-500 mr-2">
                  {{ authStore.user?.full_name }} ({{ authStore.user?.role }})
                </span>
                <router-link
                  v-if="authStore.isEmployee"
                  to="/employee/dashboard"
                  class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </router-link>
                <router-link
                  v-else-if="authStore.isEmployer"
                  to="/employer/dashboard"
                  class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </router-link>
                <button
                  @click="logout"
                  class="btn bg-red-50 text-red-600 hover:bg-red-100 border border-red-200 !px-4 !py-1.5 text-sm"
                >
                  Logout
                </button>
              </div>
            </template>
            <template v-else>
              <router-link to="/login" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                Log In
              </router-link>
              <router-link to="/register" class="btn-primary !px-4 !py-2 text-sm">
                Register
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 py-8">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <p class="text-sm text-gray-500">&copy; {{ new Date().getFullYear() }} Leave Management System. Simple & Functional.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>
