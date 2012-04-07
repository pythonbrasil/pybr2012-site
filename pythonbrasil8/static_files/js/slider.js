var Slider = new Class({
    Implements: [Options],
    options: {
        slides: []
    },
    initialize: function(options) {
        this.setOptions(options);
        this.slides = this.options.slides;
        this.show(this.index);
        this.slides.addClass('animation');
    },
    cycle: function(){
        if (this.slides.length <= 1)
            return;

        var that = this;
        setInterval(function() {
            if (that.index < that.slides.length - 1) {
                that.index = that.index + 1;
            } else {
                that.index = 0;
            }
            that.show(that.index);
        }, 4000);
    },
    next: function() {
        if (this.slides.length <= 1)
            return;

        if (this.index < this.slides.length -1) {
            this.index = this.index - 1;
        } else {
            this.index = 0;
        }
        this.show(this.index);
    },
    slides: [],
    index: 0,
    show: function(index) {
        this.index = index;
        this.slides.setStyle('opacity', 0);
        this.slides[index].setStyle('opacity', 1);
        this.slides.setStyle('z-index', '9');
        this.slides[index].setStyle('z-index', '10');
    }
});
