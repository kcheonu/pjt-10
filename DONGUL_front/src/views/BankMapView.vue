<template>
  <div class="container">
    <h1>주변 은행 검색</h1>

    <div class="d-flex align-center my-5">
      <v-select
        variant="outlined"
        color="#3CB371"
        :items="cities"
        label="광역시 / 도"
        v-model="selectedCity"
        class="mr-2"
      ></v-select>

      <v-select
        variant="outlined"
        color="#3CB371"
        :items="citiesDetail"
        label="시/군/구"
        v-model="selectedCityDetail"
        class="mx-2"
      ></v-select>

      <v-select
        variant="outlined"
        color="#3CB371"
        :items="banks"
        label="은행"
        v-model="selectedBank"
        class="mx-2"
      ></v-select>

      <v-btn
        variant="flat"
        color="#3CB371"
        size="x-large"
        @click="clickSearch"
        class="pr-7 ml-2 mb-6"
      >
        <v-icon class="me-1 mt-1">mdi-map-search-outline</v-icon>
        찾기</v-btn>
    </div>
    
    <!-- <Map
      :width="1200"
      :height="600"
      :key-word="keyword"
    /> -->
    <div class="map-container elevation-7 mb-15">
      <v-btn
        variant="text"
        color="#3CB371"
        @click="clickCurrentSearch"
        class="current-search-btn"
        rounded="xl"
        elevation="8"
        size="large"
      > 
        <v-icon class="me-1">
          mdi-reload
        </v-icon>
        현 지도에서 해당 은행 검색</v-btn>
      <div id="map" :style="`width: 1200px; height: 600px;`"></div>
    </div>


  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const dialog = ref(false)
const isDeposit = ref(false)
const chartReady = ref(false)

const selectedProduct = ref()
const selectedProductSimple = ref()
const selectedProductCode = computed(() => {
  return selectedProductSimple.value?.code
})
const isContractProduct = computed(() => {
  if (selectedProductSimple.value?.type === '정기예금'){
    return userStore.userInfo?.contract_deposit.some(e => e['deposit_code'] === selectedProductCode.value)
  } else if (selectedProductSimple.value?.type === '정기적금'){
    return userStore.userInfo?.contract_saving.some(e => e['saving_code'] === selectedProductCode.value)
  }
})

const averageIntrRateDeposit = [3.45, 4.08, 3.4, 3.35]
const intrRateDeposit = ref([null, null, null, null])
const intrRate2Deposit = ref([null, null, null, null])

const averageIntrRateSaving = [2.78, 3.62, 3.57, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])


const selectedBank = ref('전체보기')
const banks = ref(['전체보기', '우리은행', '한국스탠다드차타드은행', '대구은행', '부산은행', '광주은행', '제주은행', '전북은행', '경남은행', '중소기업은행', '한국산업은행', '국민은행', '신한은행', '농협은행', '하나은행', '수협은행'])

const selectedCity = ref()
const cities = ref(['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시', '대전광역시', '부산광역시', '서울특별시', '울산광역시', '인천시', '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도'])
const selectedCityDetail = ref()
const citiesDetail = ref()

const keyword = ref('은행')



const gangwon = ["강릉시","동해시","삼척시","속초시","원주시","춘천시","태백시","고성군","양구군","양양군","영월군","인제군","정선군","철원군","평창군","홍천군","화천군","횡성군"];
const gyeonggi = ["고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"];
const gyeongsangnam = ["거제시", "김해시", "마산시", "밀양시", "사천시", "양산시", "진주시", "진해시", "창원시", "통영시", "거창군", "고성군", "남해군", "산청군", "의령군", "창녕군", "하동군", "함안군", "함양군", "합천군"];
const gyeongsangbuk = ["경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"];
const gwangju = ["광산구", "남구", "동구", "북구", "서구"];
const daegu = ["남구", "달서구", "동구", "북구", "서구", "수성구", "중구", "달성군"];
const daejeon = ["대덕구", "동구", "서구", "유성구", "중구"];
const busan = ["강서구","금정구","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구","기장군"];
const seoul = ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"];
const ulsan = ["남구","동구","북구","중구","울주군"];
const incheon = ["계양구","남구","남동구","동구","부평구","서구","연수구","중구","강화군","옹진군"];
const jeonnam = ["광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"];
const jeonbuk = ["군산시", "김제시", "남원시", "익산시", "전주시", "정읍시", "고창군", "무주군", "부안군", "순창군", "완주군", "임실군", "장수군", "진안군"];
const jeju = ["서귀포시","제주시","남제주군","북제주군"];
const chungbuk = ["제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"];
const chungnam = ["천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"]

watch(selectedCity, () => {
  selectedCityDetail.value = null
  if (selectedCity.value == "강원도") {
    citiesDetail.value = gangwon;
  } else if (selectedCity.value == "경기도") {
    citiesDetail.value = gyeonggi;
  } else if (selectedCity.value == "경상남도") {
    citiesDetail.value = gyeongsangnam;
  } else if (selectedCity.value == "경상북도") {
    citiesDetail.value = gyeongsangbuk;
  } else if (selectedCity.value == "광주광역시") {
    citiesDetail.value = gwangju;
  } else if (selectedCity.value == "대구광역시") {
    citiesDetail.value = daegu;
  } else if (selectedCity.value == "대전광역시") {
    citiesDetail.value = daejeon;
  } else if (selectedCity.value == "부산광역시") {
    citiesDetail.value = busan;
  } else if (selectedCity.value == "서울특별시") {
    citiesDetail.value = seoul;
  } else if (selectedCity.value == "울산광역시") {
    citiesDetail.value = ulsan;
  } else if (selectedCity.value == "인천시") {
    citiesDetail.value = incheon;
  } else if (selectedCity.value == "전라남도") {
    citiesDetail.value = jeonnam;
  } else if (selectedCity.value == "전라북도") {
    citiesDetail.value = jeonbuk;
  } else if (selectedCity.value == "제주특별자치도") {
    citiesDetail.value = jeju;
  } else if (selectedCity.value == "충청남도") {
    citiesDetail.value = chungnam;
  } else if (selectedCity.value == "충청북도") {
    citiesDetail.value = chungbuk;
  }
})

watch([selectedCity, selectedCityDetail, selectedBank], () => {
  keyword.value = ''
  if (selectedCity.value) {
    keyword.value += `${selectedCity.value}`
  }
  if (selectedCityDetail.value) {
    keyword.value += `${selectedCityDetail.value}`
  }
  if (selectedBank.value) {
    if (selectedBank.value === '전체보기') {
      keyword.value += '은행'
    } else {
      keyword.value += `${selectedBank.value}`
    }
  }
})


const MAP_API_KEY = import.meta.env.VITE_MAP_API_KEY

const center = ref([37.566826, 126.9786567])
const level = ref(3)
const mapRef = ref()

onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap('init')
  } else {
    const script = document.createElement('script')

    script.onload = () => kakao.maps.load(() => initMap('init'))
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${MAP_API_KEY}&libraries=services`
    document.head.appendChild(script)
  }
})

const initMap = (state='current') => {
  // 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
  const infowindow = new kakao.maps.InfoWindow({zIndex:1});

  const mapContainer = document.getElementById('map'), // 지도를 표시할 div 
      mapOption = {
          center: new kakao.maps.LatLng(center.value[0], center.value[1]), // 지도의 중심좌표
          // level: 3 // 지도의 확대 레벨
          level: level.value // 지도의 확대 레벨
      };  

  // 지도를 생성합니다  
  if (state === 'init') {
    var map = new kakao.maps.Map(mapContainer, mapOption)
    map.setDraggable(true);
    mapRef.value = map
  } else {
    var map = mapRef.value
  }
  

  kakao.maps.event.addListener(map, 'center_changed', function() {

    // 지도의  레벨을 얻어옵니다
    const levelMap = map.getLevel();
    
    level.value = levelMap


    // 지도의 중심좌표를 얻어옵니다 
    const latlng = map.getCenter(); 
    center.value = [latlng.getLat(), latlng.getLng()]

  });

  // 장소 검색 객체를 생성합니다
  const ps = new kakao.maps.services.Places(map); 
  
  if (state !== 'search' ) {
    // 키워드에 따라 은행을 검색합니다
    if (selectedBank.value === '전체보기' || selectedBank.value === '은행') {
      ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true}); 
    } else {
      ps.keywordSearch(selectedBank.value, placesSearchCB, {useMapBounds:true});
    }
    // 키워드 검색 완료 시 호출되는 콜백함수 입니다
    function placesSearchCB (data, status, pagination) {
        if (status === kakao.maps.services.Status.OK) {
            for (var i=0; i<data.length; i++) {
                displayMarker(data[i]);    
            }       
        }
    }
  } else {
    ps.keywordSearch(keyword.value, placesSearchCB);

    // 키워드 검색 완료 시 호출되는 콜백함수 입니다
    function placesSearchCB (data, status, pagination) {

      if (status === kakao.maps.services.Status.OK) {

      // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
      // LatLngBounds 객체에 좌표를 추가합니다
      var bounds = new kakao.maps.LatLngBounds();

      for (var i=0; i<data.length; i++) {
          displayMarker(data[i]);    
          bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
      }       

      // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
      map.setBounds(bounds);
      } 
    }
  }
  
  

  // 지도에 마커를 표시하는 함수입니다
  function displayMarker(place) {
      // 마커를 생성하고 지도에 표시합니다
      const marker = new kakao.maps.Marker({
          map: map,
          position: new kakao.maps.LatLng(place.y, place.x) 
      });

      // 마커에 클릭이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'click', function() {
          // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
          infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
          infowindow.open(map, marker);
      });
  }
}


const clickSearch = function () {
  initMap('search')
  if (selectedBank.value !== '전체 보기') {
    axios({
      method: 'get',
      url: `${userStore.API_URL}/financial/get_bank_deposit/${selectedBank.value}/`
    })
      .then((res) => {
        deposits.value = []
        const results = res.data
        for (const item of results){
          deposits.value.push(makeItems(item))
        }
      })
      .catch((err) => {
        console.log(err)
      })

    axios({
      method: 'get',
      url: `${userStore.API_URL}/financial/get_bank_saving/${selectedBank.value}/`
    })
      .then((res) => {
        savings.value = []
        const results = res.data
        for (const item of results){
          savings.value.push(makeItems(item, false))
        }
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const clickCurrentSearch = function () {
  initMap()
}




</script>


<style scoped>
.container {
  width: 1200px;
  margin: 2rem auto;
  padding-top: 100px;
}

.map-container {
  position: relative;
  border-radius: 10px;
}

.current-search-btn {
  position: absolute;
  top: 10px;
  left: 50%;
  z-index: 100;
  transform: translateX(-50%);
  background-color: white;
}

#map {
  border-radius: 10px;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #3CB371;
}

</style>