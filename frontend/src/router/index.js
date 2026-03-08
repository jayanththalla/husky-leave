import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Auth/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Auth/Register.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/employee/dashboard',
    name: 'EmployeeDashboard',
    component: () => import('@/views/Employee/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'employee' },
  },
  {
    path: '/employee/apply-leave',
    name: 'ApplyLeave',
    component: () => import('@/views/Employee/ApplyLeave.vue'),
    meta: { requiresAuth: true, role: 'employee' },
  },
  {
    path: '/employer/dashboard',
    name: 'EmployerDashboard',
    component: () => import('@/views/Employer/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'employer' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.initializeFromStorage()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    next('/')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
