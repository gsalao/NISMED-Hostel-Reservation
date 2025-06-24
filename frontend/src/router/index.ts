import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
  

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/booking-form',
      name: 'booking-form',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/BookingFormView.vue'),
    },
    {
      path: '/verify',
      name: 'verify',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Verify.vue'),
    },
  ],
})

export default router