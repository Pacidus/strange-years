if FORMAT:match "gfm" then
    function Figcaption (elem)
        elem.attributes.style = "margin:auto; display: block;"
        return elem
    end
end
