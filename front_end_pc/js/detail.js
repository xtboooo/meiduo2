var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host,
        username: "",
        tab_content: {
            detail: true,
            pack: false,
            comment: false,
            service: false
        },
        sku_id: '',
        sku_count: 1,
        sku_price: price,
        cart_total_count: 0, // 购物车总数量
        carts: [], // 购物车数据
        hots: [], // 热销商品
        cat: cat, // 商品类别
        comments: [], // 评论信息
        score_classes: {
            1: 'stars_one',
            2: 'stars_two',
            3: 'stars_three',
            4: 'stars_four',
            5: 'stars_five',
        }
    },
    computed: {
        sku_amount: function(){
            return (this.sku_price * this.sku_count).toFixed(2);
        }
    },
    mounted: function(){
        this.username = Cookies.get('username');

        // 向API服务请求获取csrftoken的值并存入cookie
        this.get_csrf_token();

        // 添加用户浏览历史记录
        this.get_sku_id();

        axios.post(this.host+'/browse_histories/', {
            sku_id: this.sku_id
        },{
            responseType: 'json',
            withCredentials:true,
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            }
        })
        .then(response=>{
            console.log(response)
        })
        .catch(error=>{
            console.log(error)
        })

        this.get_cart();
        this.get_hot_goods();
        this.get_comments();
    },
    methods: {
        // 获取csrf_token的值
        get_csrf_token: function(){
            var url = this.host + "/csrf_token/";
            axios.get(url)
            .then(response => {
                // 将响应数据中的csrf_token的值存入 csrftoken cookie
                Cookies.set('csrftoken', response.data.csrf_token);
            }).catch(error => {
                console.log(error);
            })
        },
        // 退出登录按钮
        logout: function () {
            var url = this.host + '/logout/';
            axios.delete(url, {
                responseType: 'json',
                withCredentials:true,
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            })
            .then(response => {
                location.href = '/login.html';
            })
            .catch(error => {
                console.log(error.response);
            })
        },
        // 控制页面标签页展示
        on_tab_content: function(name){
            this.tab_content = {
                detail: false,
                pack: false,
                comment: false,
                service: false
            };
            this.tab_content[name] = true;
        },
        // 从路径中提取sku_id
        get_sku_id: function(){
            var re = /^\/goods\/(\d+).html$/;
            this.sku_id = document.location.pathname.match(re)[1];
        },
        // 减小数值
        on_minus: function(){
            if (this.sku_count > 1) {
                this.sku_count--;
            }
        },
         // 添加购物车
        add_cart: function(){
            var url = this.host + '/carts/'
            axios.post(url, {
                sku_id: parseInt(this.sku_id),
                count: this.sku_count
            }, {
                responseType: 'json',
                withCredentials: true,
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            })
            .then(response => {
                alert('添加购物车成功');
                this.cart_total_count += response.data.count;
            })
            .catch(error => {
                console.log(error);
            })
        },
        get_cart: function (){
            var url = this.host + '/carts/simple/';
            axios.get(url, {
                responseType: 'json',
                withCredentials:true,
            })
            .then(response => {
                this.carts = response.data.cart_skus;
                this.cart_total_count = 0;
                for(let i=0;i<this.carts.length;i++){
                    if (this.carts[i].name.length>25){
                        this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                    }
                    this.cart_total_count += this.carts[i].count;
                }
            })
            .catch(error => {
                console.log(error);
            })
        },
        // 获取热销商品数据
        get_hot_goods: function(){
            // 请求获取热销商品数据
            var url = this.host+'/hot/'+this.cat + '/'
            axios.get(url, {
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                 this.hots = response.data.hot_skus
                 for(let i=0; i<this.hots.length; i++){
                    this.hots[i].url = '/goods/' + this.skus[i].id + ".html";
                }
            })
            .catch(error => {
                console.log(error);
            })
        },
        // 获取商品评价信息
        get_comments: function(){

        }
    }
});
