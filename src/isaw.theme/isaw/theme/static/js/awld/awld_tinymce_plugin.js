(function() {
  tinymce.create('tinymce.plugins.awldjs', {
    init : function(ed, url) {
      ed.addCommand('awldjs', function() {
        try {
          ed.focus();
          var $node = $(ed.selection.getNode());
          if ($node.length && !$node.hasClass('awld-scope') && !$node.parents('.awld-scope').length) {
            var $output = $('<div></div>').html($('<div class="awld-scope"></div>').html($node));
            ed.execCommand('mceInsertContent', false, $output.html());
          }
        } catch(e) {
          alert('Whoops. Something went wrong!');
        }
      });

      // Register example button
      ed.addButton('awldjs', {
        title : 'Enable AWLD.js',
        text: 'AWLD',
        cmd : 'awldjs',
        image: '/++theme++isaw.theme/images/light-bulb-code.png',
        tooltip: 'Enable AWLD.js on selection'
      });
    }
  });
  tinymce.PluginManager.add('awldjs', tinymce.plugins.awldjs);
})();
