describe("Slider", function(){
    var slider;

    beforeEach(function(){
        slider = new Slider({slides: $$('#sponsors .row')});
    });

    it("should set slides with option.slides value", function(){
        expect(slider.slides).toBe(slider.options.slides);
    });

    it("should have 2 slides", function(){
        expect(slider.slides.length).toBe(2);
    });

    it("index should be 0", function(){
        expect(slider.index).toBe(0);
    });

    it("first row should be opacity 1", function(){
        expect(slider.slides[0].getStyle('opacity')).toBe(1);
    });

    it("first row should be with z-index 10", function(){
        expect(slider.slides[0].getStyle('z-index')).toBe('10');
    });

    it("second row should be with z-index 9", function(){
        expect(slider.slides[1].getStyle('z-index')).toBe('9');
    });

    it("second row should be opacity 0", function(){
        expect(slider.slides[1].getStyle('opacity')).toBe(0);
    });

    describe("when show slide is called with index 1", function() {
        beforeEach(function(){
            slider.show(1);
        });

        it("second row should be opacity 1", function(){
            expect(slider.slides[1].getStyle('opacity')).toBe(1);
        });

        it("first row should be opacsty 0", function(){
            expect(slider.slides[0].getStyle('opacity')).toBe(0);
        });

        it("first row should be with z-index 9", function(){
            expect(slider.slides[0].getStyle('z-index')).toBe('9');
        });

        it("second row should be with z-index 10", function(){
            expect(slider.slides[1].getStyle('z-index')).toBe('10');
        });

        it("index should be 1", function(){
            expect(slider.index).toBe(1);
        });
    });


});
