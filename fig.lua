if FORMAT:match "gfm" then
    function Figure (elem)
        return {
        pandoc.RawInline("html", "<p align='center'>"),
        elem,
        pandoc.RawInline("html", "</p>")
        }
    end
end
