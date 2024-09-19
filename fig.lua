if FORMAT:match "gfm" then
    --[[
    function Figcaptionqq (elem)
        return {
        pandoc.RawInline("html", "<p align='center'>"),
        elem,
        pandoc.RawInline("html", "</p>")
        }
    end
    --]]

    function Figure (elem)
        elem.attributes.style = 'text-align: center; margin:auto; display: block'

        return elem 
    end

    function Image (elem)
        elem.attributes.style = 'margin:auto; display: block;'
        return elem
    end
end



